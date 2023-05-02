from viewser import Queryset, Column
import numpy as np
import pandas as pd
from sklearn import decomposition
from sklearn.decomposition import PCA
import cm_querysets
import pgm_querysets
import ModelDefinitions
from ingester3.ViewsMonth import ViewsMonth
from ingester3.Country import Country
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def get_fatalities(level: str, dev_id: str, EndOfHistory: int) -> pd.DataFrame:
    """
    Gathers the number of fatalities 36 months before and after the EndOfHistory in a Pandas DataFrame
    
    Example: fatalities = get_fatalities(level=level, dev_id=dev_id, EndOfHistory=EndOfHistory)
    """
    qs1 = (Queryset("actuals_monthly", "country_month")
            .with_column(Column("ged_best_sb", from_table= "ged2_cm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.fill())   
            .with_theme("fatalities")
            .describe(""" Fatalities conflict history, cm level Monthly Update"""))
    actuals = qs1.publish().fetch()

    actuals = actuals.loc[EndOfHistory-40:EndOfHistory]
    actuals = actuals.reset_index()
    actuals['step'] = actuals['month_id'] - EndOfHistory
    actuals = actuals.set_index(['step', 'country_id'], drop=True)
    actuals.rename(columns={'ged_best_sb':'fatalities'}, inplace=True)

    predstore_future = level +  '_' + 'genetic_ensemble' + '_f' + str(EndOfHistory)
    predictions_df = pd.DataFrame.forecasts.read_store(predstore_future, run=dev_id)

    predictions_df = predictions_df.reset_index()
    predictions_df['step'] = predictions_df['month_id'] - EndOfHistory
    predictions_df = predictions_df.set_index(['step', 'country_id'], drop=True)
    predictions_df['step_combined'] = np.expm1(predictions_df['step_combined'])
    predictions_df.rename(columns={'step_combined':'fatalities'}, inplace=True)

    merge = pd.concat([actuals, predictions_df], axis=0)
    
    
    def cid2name(country_id):
        name = Country(country_id).name
        return name
       
    merge = merge.reset_index(drop=False)
    c_id = [int(x) for x in merge['country_id']] 
    country_names = [Country(x).name for x in c_id]
    merge['country'] = country_names
    
    merge = merge.set_index(['step', 'country_id'], drop=True)
    
    return merge


def get_fatcat(merge, rolling_months_prior):
    fatcat = merge.copy()
    fatcat = fatcat.reset_index(drop=False)

    def ged_fatalities(x):
        if x < 0.5:
            return 0
        elif x < 10:
            return 1
        elif x < 100:
            return 2
        elif x < 1000:
            return 3
        else:
            return 4

    def ged_intensity_lvl(x):
        if x < 0.5:
            return 0
        elif x < 100:
            return 1
        else:
            return 2

    fatcat['fatcat'] = fatcat['fatalities'].apply(ged_fatalities)

    fatcat['fatcat_change'] = fatcat.groupby('country_id')['fatcat'].diff()

    fatcat['fatcat_change'] = fatcat['fatcat_change'].fillna(0)

    fatcat = fatcat.set_index(['step','country_id'], drop=True)

    fatcat['fatcat_nominal'] = fatcat['fatcat']
    fatcat = fatcat.reset_index()

    fat_classes = [
        (fatcat['fatcat'] == 0), 
        (fatcat['fatcat'] == 1),
        (fatcat['fatcat'] == 2),
        (fatcat['fatcat'] == 3),
        (fatcat['fatcat'] == 4)
    ]

    fat_categories = ['Non-violent', 'Low Violence', 'Violence', 'High-violence', 'Extreme Violence']

    fatcat['fatcat_nominal'] = np.select(fat_classes, fat_categories)

    fatcat = fatcat.set_index(['step','country_id'], drop=True)

    fatcat['monthly_change'] = fatcat['fatcat_change']
    fatcat = fatcat.reset_index()

    violence_conditions = [
        (fatcat['monthly_change'] == -4),
        (fatcat['monthly_change'] == -3), 
        (fatcat['monthly_change'] == -2), 
        (fatcat['monthly_change'] == -1),
        (fatcat['monthly_change'] == 0),
        (fatcat['monthly_change'] == 1),
        (fatcat['monthly_change'] == 2),
        (fatcat['monthly_change'] == 3),
        (fatcat['monthly_change'] == 4)
    ]

    violence_categories = ['Extreme Descalation', 'Rapid De-escalation', 'De-escalation', 
                           'Low De-escalation', 'Status Quo','Low Escalation',
                          'Escalation','Rapid Escalation','Extreme Escalation']

    fatcat['monthly_change'] = np.select(violence_conditions, violence_categories)

    # This creates a rolling mean of the violence over the past 'months prior' parameter
    fatcat['rolling_mean_violence'] = fatcat.groupby('country_id')['fatalities'].transform(lambda x: x.shift(1).rolling(rolling_months_prior, 1).mean())

    fatcat['intensity_lvl'] = fatcat['rolling_mean_violence'].apply(ged_intensity_lvl)

    fatcat = fatcat.loc[fatcat['step'] >= -36]
    fatcat = fatcat.set_index(['step', 'country_id'], drop=True)
    
    return fatcat


def get_fatcat_list(fatcat, step_value, step_value2):
    fatcat_step = f'fatcat_{step_value}'  # dynamic variable name
    fatcat_step = fatcat.reset_index(drop=False)
    fatcat_step = fatcat_step[fatcat_step['step'] == step_value] 
    fatcat_step_pivot = pd.pivot_table(fatcat_step, values=['fatalities','fatcat', 'fatcat_nominal', 'fatcat_change', 'monthly_change', 'rolling_mean_violence', 'intensity_lvl'], index=['country_id'])
    fatcat_step_pivot.rename(columns={f'fatalities': f'fatalities_step_{step_value}'}, inplace=True)
    fatcat_step_pivot.rename(columns={f'fatcat': f'fatcat_step_{step_value}'}, inplace=True)

    fatcat_step2 = f'fatcat_{step_value2}'  # dynamic variable name
    fatcat_step2 = fatcat.reset_index(drop=False)
    fatcat_step2 = fatcat_step2[fatcat_step2['step'] == step_value2] 
    fatcat_step2_pivot = pd.pivot_table(fatcat_step2, values=['fatalities','fatcat', 'fatcat_nominal', 'fatcat_change', 'monthly_change', 'rolling_mean_violence', 'intensity_lvl'], index=['country_id'])
    fatcat_step2_pivot.rename(columns={f'fatalities': f'fatalities_step_{step_value2}'}, inplace=True)
    fatcat_step2_pivot.rename(columns={f'fatcat': f'fatcat_step_{step_value2}'}, inplace=True)

    fatcat_list = fatcat_step_pivot.join(fatcat_step2_pivot, lsuffix=f'_step_{step_value}', rsuffix=f'_step_{step_value2}')
    fatcat_list = fatcat_list.sort_values(f'fatalities_step_{step_value}', ascending=False)

    fatcat_list['fatcat_change'] = fatcat_list[f'fatcat_step_{step_value2}'] - fatcat_list[f'fatcat_step_{step_value}']

    violence_conditions2 = [
        (fatcat_list['fatcat_change'] == -4),
        (fatcat_list['fatcat_change'] == -3), 
        (fatcat_list['fatcat_change'] == -2), 
        (fatcat_list['fatcat_change'] == -1),
        (fatcat_list['fatcat_change'] == 0),
        (fatcat_list['fatcat_change'] == 1),
        (fatcat_list['fatcat_change'] == 2),
        (fatcat_list['fatcat_change'] == 3),
        (fatcat_list['fatcat_change'] == 4)
    ]

    violence_categories = ['Extreme Descalation', 'Rapid De-escalation', 'De-escalation', 
                           'Low De-escalation', 'Status Quo','Low Escalation',
                          'Escalation','Rapid Escalation','Extreme Escalation']

    fatcat_list['facat_change_nominal'] = np.select(violence_conditions2, violence_categories)
    return fatcat_list


def clean_list(fatcat_list, step_value, step_value2):

    def cid2name(country_id):
        name = Country(country_id).name
        return name
        
    # Add country names
    fatcat_list = fatcat_list.reset_index(drop=False)
    c_id = [int(x) for x in fatcat_list['country_id']] 
    country_names = [Country(x).name for x in c_id]
    fatcat_list['country'] = country_names
    fatcat_list = fatcat_list.set_index('country_id', drop=True)

    # Create Fatcat list 0 nominal
    fatcat_list[f'fatcat_step_{step_value}_nominal'] = fatcat_list[f'fatcat_step_{step_value}']
    fatcat_list = fatcat_list.reset_index()
    fat_classes = [
        (fatcat_list[f'fatcat_step_{step_value}'] == 0), 
        (fatcat_list[f'fatcat_step_{step_value}'] == 1),
        (fatcat_list[f'fatcat_step_{step_value}'] == 2),
        (fatcat_list[f'fatcat_step_{step_value}'] == 3),
        (fatcat_list[f'fatcat_step_{step_value}'] == 4)
    ]
    fat_categories = ['Non-violent', 'Low Violence', 'Violent', 'High-violence', 'Extreme Violence']
    fatcat_list[f'fatcat_step_{step_value}_nominal'] = np.select(fat_classes, fat_categories)
    fatcat_list = fatcat_list.set_index(['country_id'], drop=True)

    # Create Fatcat list 12 nominal
    fatcat_list[f'fatcat_step_{step_value2}_nominal'] = fatcat_list[f'fatcat_step_{step_value2}']
    fatcat_list = fatcat_list.reset_index()
    fat_classes = [
        (fatcat_list[f'fatcat_step_{step_value2}'] == 0), 
        (fatcat_list[f'fatcat_step_{step_value2}'] == 1),
        (fatcat_list[f'fatcat_step_{step_value2}'] == 2),
        (fatcat_list[f'fatcat_step_{step_value2}'] == 3),
        (fatcat_list[f'fatcat_step_{step_value2}'] == 4)
    ]
    fat_categories = ['Non-violent', 'Low Violence', 'Violent', 'High-violence', 'Extreme Violence']
    fatcat_list[f'fatcat_step_{step_value2}_nominal'] = np.select(fat_classes, fat_categories)
    fatcat_list = fatcat_list.set_index(['country_id'], drop=True)

    return fatcat_list

def get_escalation_list(fatcat_list, step_value2):
    escalation_list = fatcat_list.copy()
    escalation_list = escalation_list.loc[escalation_list['fatcat_change'] >= 1 ]
    escalation_list = escalation_list.set_index('country', drop=True)
    escalation_list = escalation_list.sort_values(by = [f'fatalities_step_{step_value2}'], ascending=[False])
    return escalation_list

def get_deescalation_list(fatcat_list, step_value2):
    deescalation_list = fatcat_list.copy()
    deescalation_list = deescalation_list.loc[deescalation_list['fatcat_change'] < 0 ]
    deescalation_list = deescalation_list.set_index('country', drop=True)
    deescalation_list = deescalation_list.sort_values(by = [f'fatalities_step_{step_value2}'], ascending=[False])
    return deescalation_list

def get_nochange_list(fatcat_list, step_value2):
    nochange_list = fatcat_list.copy()
    nochange_list = nochange_list.loc[nochange_list['fatcat_change'] == 0 ]
    nochange_list = nochange_list.set_index('country', drop=True)
    nochange_list = nochange_list.sort_values(by = [f'fatalities_step_{step_value2}'], ascending=[False])
    return nochange_list


def get_escalation_shortlist(escalationlist, step_value, step_value2):
    shortlist = escalationlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}', 'facat_change_nominal']].copy()
    shortlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}']] = shortlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}']].applymap(lambda x: math.ceil(x))
    return shortlist


def get_deescalation_shortlist(deescalationlist, step_value, step_value2):
    shortlist = deescalationlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}', 'facat_change_nominal']].copy()
    shortlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}']] = shortlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}']].applymap(lambda x: math.ceil(x))
    return shortlist

def get_nochange_shortlist(nochangelist, step_value, step_value2):
    shortlist = nochangelist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}', 'facat_change_nominal']].copy()
    shortlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}']] = shortlist[[f'fatalities_step_{step_value}', f'fatalities_step_{step_value2}']].applymap(lambda x: math.ceil(x))
    return shortlist



def fatcat_compare(fatcat, step_value, step_value2):
    fatcat_step = f'fatcat_{step_value}'  
    fatcat_step = fatcat.reset_index(drop=False)
    fatcat_step = fatcat_step[fatcat_step['step'] == step_value] 
    fatcat_step_pivot = pd.pivot_table(fatcat_step, values=['fatalities','fatcat', 'fatcat_nominal', 'fatcat_change', 'monthly_change', 'rolling_mean_violence', 'intensity_lvl'], index=['country_id'])
    fatcat_step_pivot.rename(columns={f'fatalities': f'fatalities_step_{step_value}'}, inplace=True)
    fatcat_step_pivot.rename(columns={f'fatcat': f'fatcat_step_{step_value}'}, inplace=True)

    fatcat_step2 = f'fatcat_{step_value2}'  # dynamic variable name
    fatcat_step2 = fatcat.reset_index(drop=False)
    fatcat_step2 = fatcat_step2[fatcat_step2['step'] == step_value2] 
    fatcat_step2_pivot = pd.pivot_table(fatcat_step2, values=['fatalities','fatcat', 'fatcat_nominal', 'fatcat_change', 'monthly_change', 'rolling_mean_violence', 'intensity_lvl'], index=['country_id'])
    fatcat_step2_pivot.rename(columns={f'fatalities': f'fatalities_step_{step_value2}'}, inplace=True)
    fatcat_step2_pivot.rename(columns={f'fatcat': f'fatcat_step_{step_value2}'}, inplace=True)

    fatcat_list = fatcat_step_pivot.join(fatcat_step2_pivot, lsuffix=f'_step_{step_value}', rsuffix=f'_step_{step_value2}')
    fatcat_list = fatcat_list.sort_values(f'fatalities_step_{step_value}', ascending=False)

    fatcat_list['fatcat_change'] = fatcat_list[f'fatcat_step_{step_value2}'] - fatcat_list[f'fatcat_step_{step_value}']

    violence_conditions2 = [
        (fatcat_list['fatcat_change'] == -4),
        (fatcat_list['fatcat_change'] == -3), 
        (fatcat_list['fatcat_change'] == -2), 
        (fatcat_list['fatcat_change'] == -1),
        (fatcat_list['fatcat_change'] == 0),
        (fatcat_list['fatcat_change'] == 1),
        (fatcat_list['fatcat_change'] == 2),
        (fatcat_list['fatcat_change'] == 3),
        (fatcat_list['fatcat_change'] == 4)
    ]

    violence_categories = ['Extreme Descalation', 'Rapid De-escalation', 'De-escalation', 
                           'Low De-escalation', 'Status Quo','Low Escalation',
                          'Escalation','Rapid Escalation','Extreme Escalation']

    fatcat_list['facat_change_nominal'] = np.select(violence_conditions2, violence_categories)

    def cid2name(country_id):
        name = Country(country_id).name
        return name
        
    # Add country names
    fatcat_list = fatcat_list.reset_index(drop=False)
    c_id = [int(x) for x in fatcat_list['country_id']] 
    country_names = [Country(x).name for x in c_id]
    fatcat_list['country'] = country_names
    fatcat_list = fatcat_list.set_index('country_id', drop=True)

    # Create Fatcat list 0 nominal
    fatcat_list[f'fatcat_step_{step_value}_nominal'] = fatcat_list[f'fatcat_step_{step_value}']
    fatcat_list = fatcat_list.reset_index()
    fat_classes = [
        (fatcat_list[f'fatcat_step_{step_value}'] == 0), 
        (fatcat_list[f'fatcat_step_{step_value}'] == 1),
        (fatcat_list[f'fatcat_step_{step_value}'] == 2),
        (fatcat_list[f'fatcat_step_{step_value}'] == 3),
        (fatcat_list[f'fatcat_step_{step_value}'] == 4)
    ]
    fat_categories = ['Non-violent', 'Low Violence', 'Violent', 'High-violence', 'Extreme Violence']
    fatcat_list[f'fatcat_step_{step_value}_nominal'] = np.select(fat_classes, fat_categories)
    fatcat_list = fatcat_list.set_index(['country_id'], drop=True)

    # Create Fatcat list 12 nominal
    fatcat_list[f'fatcat_step_{step_value2}_nominal'] = fatcat_list[f'fatcat_step_{step_value2}']
    fatcat_list = fatcat_list.reset_index()
    fat_classes = [
        (fatcat_list[f'fatcat_step_{step_value2}'] == 0), 
        (fatcat_list[f'fatcat_step_{step_value2}'] == 1),
        (fatcat_list[f'fatcat_step_{step_value2}'] == 2),
        (fatcat_list[f'fatcat_step_{step_value2}'] == 3),
        (fatcat_list[f'fatcat_step_{step_value2}'] == 4)
    ]
    fat_categories = ['Non-violent', 'Low Violence', 'Violent', 'High-violence', 'Extreme Violence']
    fatcat_list[f'fatcat_step_{step_value2}_nominal'] = np.select(fat_classes, fat_categories)
    fatcat_list = fatcat_list.set_index(['country_id'], drop=True)

    return fatcat_list


def plot_pastfuture(df, country_id):
    
    df = df.copy()
    df = df.reset_index(drop=False)
    df = df.loc[df['step'] >= -36]
    df['fatalities_log1p'] = np.log1p(df['fatalities'])
    
    # Filter the DataFrame to include only the specified country
    country_df = df[df['country_id'] == country_id]

    # Get the country name from the 'country' column
    country_name = country_df['country'].iloc[0]

    fig, ax = plt.subplots(figsize=(18, 3))

    ax.plot(country_df.loc[country_df['step'] <= 0, 'step'], country_df.loc[country_df['step'] <= 0, 'fatalities'], color='darkorange', label='Actuals')
    ax.plot(country_df.loc[country_df['step'] >= 0, 'step'], country_df.loc[country_df['step'] >= 0, 'fatalities'], color='cornflowerblue', label='Predictions')

    ax.axvline(x=0, color='lightcoral', linestyle='--')

    ax.xaxis.grid(True, which="both", color="#cccccc", alpha=0.3, lw=0.9)
    ax.yaxis.grid(True, which="both", color="#cccccc", alpha=0.3, lw=0.9)

    ax.text(0, 1.13, f'Number of Reported and Predicted Fatalities for {country_name}', weight="bold", size=20, transform=ax.transAxes)    
    ax.set_xlabel('Months from present', fontsize=15)
    ax.set_ylabel('Fatalities (log+1)', fontsize=15)

    ax.set_xlim(-36, 36)
    ax.set_xticks([-36, -30, -33, -27,-24, -21, -18, -15, -12, -9, -6, -3, 0, 3, 6, 9,12, 15, 18, 21,24, 27,30, 33, 36])

    ax.set_ylim(bottom=0)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    ax.legend()
    
    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_visible(False)

    
    plt.show()
    
def plot_pastfuture_log(df, country_id):
    
    df = df.copy()
    df = df.reset_index(drop=False)
    df = df.loc[df['step'] >= -36]
    df['fatalities_log1p'] = np.log1p(df['fatalities'])
    
    # Filter the DataFrame to include only the specified country
    country_df = df[df['country_id'] == country_id]

    # Get the country name from the 'country' column
    country_name = country_df['country'].iloc[0]
    
    fig, ax = plt.subplots(figsize=(14, 3))
    plt.style.use("seaborn-whitegrid")  
    # Plot the y-axis based on the condition
    if country_df['fatalities'].max() > 1000:
        ax.plot(country_df.loc[country_df['step'] <= 0, 'step'], country_df.loc[country_df['step'] <= 0, 'fatalities_log1p'], color='cornflowerblue', label='Reported Fatalities')
        ax.plot(country_df.loc[country_df['step'] >= 0, 'step'], country_df.loc[country_df['step'] >= 0, 'fatalities_log1p'], color='darkorange', label='Predicted Fatalities')
        ax.set_ylabel('Fatalities', fontsize=15)
        
        # Set a custom formatter for the y-axis labels
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{np.round(np.expm1(x), 0):,.0f}'))
    else:
        ax.plot(country_df.loc[country_df['step'] <= 0, 'step'], country_df.loc[country_df['step'] <= 0, 'fatalities'], color='cornflowerblue', label='Actuals')
        ax.plot(country_df.loc[country_df['step'] >= 0, 'step'], country_df.loc[country_df['step'] >= 0, 'fatalities'], color='darkorange', label='Predictions')
    ax.set_ylabel('Fatalities', fontsize=15)

    ax.axvline(x=0, color='lightcoral', linestyle='--')

    ax.xaxis.grid(True, which="both", color="#cccccc", alpha=0.3, lw=0.9)
    ax.yaxis.grid(True, which="both", color="#cccccc", alpha=0.3, lw=0.9)

    ax.text(0, 1.13, f'Number of reported and predicted fatalities for {country_name}', weight="bold", size=20, transform=ax.transAxes)    
    ax.set_xlabel('Months from present', fontsize=15)

    ax.set_xlim(-36, 36)
    ax.set_xticks([-36, -30, -33, -27,-24, -21, -18, -15, -12, -9, -6, -3, 0, 3, 6, 9,12, 15, 18, 21,24, 27,30, 33, 36])

    ax.set_ylim(bottom=0)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    ax.legend()
    
    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_visible(False)

    plt.show()


def plot_fatcat(df, country_id):
    df = df.copy()
    df = df.reset_index(drop=False)
    df = df[df['country_id'] == country_id]

    country_name = df['country'].iloc[0]

    fig, ax = plt.subplots(figsize=(14, 3))
    ax2 = ax.twinx()
    
    ax.plot(df.loc[df['step'] <= 0, 'step'], df.loc[df['step'] <= 0, 'fatcat'], color='cornflowerblue', label='Past')
    ax.plot(df.loc[df['step'] >= 0, 'step'], df.loc[df['step'] >= 0, 'fatcat'], color='darkorange', label='Future')

    ax2.plot(df['step'], df['fatalities'], color='forestgreen', label='Fatalities', alpha=0.2, lw=0.9)
    
    ax.axvline(x=0, color='lightcoral', linestyle='--')


    ax.xaxis.grid(True, which="both", color="#cccccc", alpha=0.3, lw=0.9)
    ax.yaxis.grid(True, which="both", color="#cccccc", alpha=0.3, lw=0.9)

    ax.text(.3, 1.08, f'Fatality Category for {country_name}', weight="bold", size=20, transform=ax.transAxes)    
    ax.set_xlabel('Months from present', fontsize=15)
    ax.set_ylabel('Fatalities Category', fontsize=15)
    ax2.set_ylabel('Number of Fatalities', fontsize=15)
    
    ax.set_ylim(-5, 5)
    ax.set_xlim(-36, 36)
    ax.set_xticks([-36, -30, -33, -27,-24, -21, -18, -15, -12, -9, -6, -3, 0, 3, 6, 9,12, 15, 18, 21,24, 27,30, 33, 36])

    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='best')
    
    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_visible(False)
    
    plt.show()

def vid2date(i):
    year=str(ViewsMonth(i).year)
    month=str(ViewsMonth(i).month)
    return year+'/'+monthb


