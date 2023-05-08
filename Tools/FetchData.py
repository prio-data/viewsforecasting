
from viewser import Queryset, Column
import numpy as np
import pandas as pd
from sklearn import decomposition
from sklearn.decomposition import PCA
import cm_querysets
import pgm_querysets
import ModelDefinitions


def ReturnQsList(level):
    if level == 'cm':
        return cm_querysets.get_cm_querysets()
    elif level == 'pgm':
        return pgm_querysets.get_pgm_querysets()
    else:
        raise Exception(f'unrecognised level {level}')


def SummarizeTable(dfname,df):
    print(f"{dfname}: A dataset with {len(df.columns)} columns, with "
          f"data between t = {min(df.index.get_level_values(0))} "
          f"and {max(df.index.get_level_values(0))}; "
          f"{len(np.unique(df.index.get_level_values(1)))} units."
          )


def FetchTable(Queryset, name):
    df = Queryset.fetch().astype(float)
    df.name = name
    SummarizeTable(name,df)
    data = {
            'Name': name,
            'df': df
        }
    return data


def FetchData(run_id, EndOfPCAData):
    print(f'Fetching data using querysets; {run_id}; returns as list of dictionaries containing datasets')
    Datasets = []

    if run_id == 'Fatalities001':
        Datasets.append(FetchTable((Queryset("hh_fatalities_ged_ln_ultrashort", "country_month")), 'baseline'))
        Datasets.append(FetchTable((Queryset("hh_fatalities_ged_acled_ln", "country_month")), 'conflictlong_ln'))
        Datasets.append(FetchTable((Queryset("fat_cm_conflict_history", "country_month")), 'conflict_ln'))
        Datasets.append(FetchTable((Queryset("fat_cm_conflict_history_exp", "country_month")), 'conflict_nolog'))
        Datasets.append(FetchTable((Queryset("hh_fatalities_wdi_short", "country_month")), 'wdi_short'))
        Datasets.append(FetchTable((Queryset("hh_fatalities_vdem_short", "country_month")), 'vdem_short'))
        Datasets.append(FetchTable((Queryset("hh_topic_model_short", "country_month")), 'topics_short'))
        Datasets.append(FetchTable((Queryset("hh_broad", "country_month")), 'broad'))
        #        Datasets.append(FetchTable((Queryset("hh_prs", "country_month")),'prs'))
        Datasets.append(FetchTable((Queryset("hh_greatest_hits", "country_month")), 'gh'))
        Datasets.append(FetchTable((Queryset("hh_20_features", "country_month")), 'hh20'))
        Datasets.append(FetchTable((Queryset("hh_all_features", "country_month")), 'all_features'))

        # PCA
        Standard_features = ['ln_ged_sb_dep', 'ln_ged_sb', 'decay_ged_sb_5', 'decay_ged_os_5', 'splag_1_decay_ged_sb_5',
                             'wdi_sp_pop_totl']

        sources = []
        af = {
            'name': 'all features',
            'dataset': Datasets[10]['df'],
            'n_comp': 20
        }
        sources.append(af)
        topics = {
            'name': 'topics',
            'dataset': Datasets[6]['df'],
            'n_comp': 10
        }
        sources.append(topics)
        vdem = {
            'name': 'vdem',
            'dataset': Datasets[5]['df'],
            'n_comp': 15
        }
        sources.append(vdem)
        wdi = {
            'name': 'wdi',
            'dataset': Datasets[4]['df'],
            'n_comp': 15
        }
        sources.append(wdi)

        for source in sources:
            source = PCA(source, Standard_features, EndOfPCAData)

        Data = {
            'Name': 'pca_all',
            'df': af['result']
        }
        Datasets.append(Data)

        Data = {
            'Name': 'pca_topics',
            'df': topics['result']
        }
        Datasets.append(Data)

        Data = {
            'Name': 'pca_vdem',
            'df': vdem['result']
        }
        Datasets.append(Data)

        Data = {
            'Name': 'pca_wdi',
            'df': wdi['result']
        }
        Datasets.append(Data)

    elif run_id == 'Fatalities002':
        Datasets.append(FetchTable((Queryset("fatalities002_baseline", "country_month")),'baseline002'))
        Datasets.append(FetchTable((Queryset("fatalities002_conflict_history_long", "country_month")),'conflictlong_ln'))
        Datasets.append(FetchTable((Queryset("fatalities002_conflict_history", "country_month")),'conflict_ln'))
        Datasets.append(FetchTable((Queryset("fatalities002_wdi_short", "country_month")),'wdi_short'))
        Datasets.append(FetchTable((Queryset("fatalities002_vdem_short", "country_month")),'vdem_short'))
        Datasets.append(FetchTable((Queryset("fatalities002_topics", "country_month")),'topics_002'))
        Datasets.append(FetchTable((Queryset("fatalities002_joint_broad", "country_month")),'joint_broad'))
        Datasets.append(FetchTable((Queryset("fatalities002_joint_narrow", "country_month")),'joint_narrow'))
        Datasets.append(FetchTable((Queryset("fatalities002_all_features", "country_month")),'all_features'))
        Datasets.append(FetchTable((Queryset("fatalities002_aquastat", "country_month")),'aquastat'))
        Datasets.append(FetchTable((Queryset("fatalities002_faostat", "country_month")),'faostat'))
        Datasets.append(FetchTable((Queryset("fatalities002_faoprices", "country_month")),'faoprices'))
        Datasets.append(FetchTable((Queryset("fatalities002_imfweo", "country_month")),'imfweo'))

        # PCA
        Standard_features = ['ln_ged_sb_dep','ln_ged_sb', 'decay_ged_sb_5', 'decay_ged_os_5', 'splag_1_decay_ged_sb_5', 'wdi_sp_pop_totl']

        sources = []
        af = {
            'name': 'all features',
            'dataset': Datasets[8]['df'],
            'n_comp': 20
        }
        sources.append(af)

        topics = {
            'name': 'topics',
            'dataset': Datasets[5]['df'],
            'n_comp': 10
        }
        sources.append(topics)

        vdem = {
            'name': 'vdem',
            'dataset': Datasets[4]['df'],
            'n_comp': 15
        }
        sources.append(vdem)

        wdi = {
            'name': 'wdi',
            'dataset': Datasets[3]['df'],
            'n_comp': 15
        }
        sources.append(wdi)

        for source in sources:
            source = PCA(source, Standard_features,EndOfPCAData)

        Data = {
            'Name': 'pca_all',
            'df': af['result']
        }
        Datasets.append(Data)

        Data = {
            'Name': 'pca_topics',
            'df': topics['result']
        }
        Datasets.append(Data)

        Data = {
            'Name': 'pca_vdem',
            'df': vdem['result']
        }
        Datasets.append(Data)

        Data = {
            'Name': 'pca_wdi',
            'df': wdi['result']
        }
        Datasets.append(Data)

##################################################################################################################################
### From here Chandler needs to add the models as he goes
### simply follow the examples from below. 
### Match the queryset calls and append them
##################################################################################################################################
        
    elif run_id == 'escwa001':
        Datasets.append(FetchTable((Queryset("qs_cm_cflong", "country_month")),'cflong'))
        Datasets.append(FetchTable((Queryset("qs_vdem_escwa", "country_month")),'vdem'))
        Datasets.append(FetchTable((Queryset("qs_wdi_escwa", "country_month")),'wdi'))
        Datasets.append(FetchTable((Queryset("qs_aquastat_escwa", "country_month")),'aquastat'))
        Datasets.append(FetchTable((Queryset("qs_food_escwa", "country_month")),'food'))
        Datasets.append(FetchTable((Queryset("qs_imfweo_escwa", "country_month")),'imfweo'))
        Datasets.append(FetchTable((Queryset("qs_faostat_escwa", "country_month")),'faostat'))
        Datasets.append(FetchTable((Queryset("qs_escwa_broad", "country_month")),'broad'))
        Datasets.append(FetchTable((Queryset("qs_escwa_onset", "country_month")),'onset'))


    else:
        raise Exception(f"run_id {run_id} not recognised")

    return(Datasets)


def get_df_from_datasets_by_name(Datasets,name):
    for ds in Datasets:
        if name in ds['Name']:
            return ds['df']
    else:
        raise Exception('No Dataset similar to ',name,'found')


def fetch_cm_data_from_model_def(qslist, EndOfPCAData):

    level = 'cm'

    ModelList = ModelDefinitions.DefineEnsembleModels(level)

    defined_querysets=[qs.name for qs in qslist]

    model_querysets=list(set([model['queryset'] for model in ModelList]))

    qs_short_names={}
    for model in ModelList:
        qs_short_names[model['queryset']]=model['data_train']

    Datasets=[]

    for model_qs in model_querysets:
        if model_qs not in defined_querysets:
            raise Exception(f'queryset',model_qs,'is not defined in the imported queryset definitions file')

        Datasets.append(FetchTable((Queryset(model_qs, "country_month")), qs_short_names[model_qs]))

    # PCA
    Standard_features = ['ln_ged_sb_dep', 'ln_ged_sb', 'decay_ged_sb_5', 'decay_ged_os_5', 'splag_1_decay_ged_sb_5',
                         'wdi_sp_pop_totl']

    sources = []
    
    for name in ['cflong']:
        src = {
            'name': name,
            'dataset': get_df_from_datasets_by_name(Datasets,name),
            'n_comp': 20
             }
        sources.append(src)


    return Datasets


def FetchData_pgm(run_id):
    print('Fetching data using querysets; returns as list of dictionaries containing datasets')
    Datasets = []
    if run_id == 'Fatalities001':
        Datasets.append(FetchTable((Queryset("hh_fat_pgm_baseline", "priogrid_month")),'baseline'))
        Datasets.append(FetchTable((Queryset("hh_fat_pgm_conflictlong", "priogrid_month")),'conflictlong'))
        Datasets.append(FetchTable((Queryset("fat_escwa_drought_vulnerability_pgm", "priogrid_month")),'escwa_drought'))
        Datasets.append(FetchTable((Queryset("hh_fat_pgm_natsoc", "priogrid_month")),'natsoc'))
        Datasets.append(FetchTable((Queryset("hh_fat_pgm_broad", "priogrid_month")),'broad'))
        Datasets.append(FetchTable((Queryset("paola_fatalities_conflict_history", "priogrid_month")),'paola_conf_hist'))
        Datasets.append(FetchTable((Queryset("jim_pgm_conflict_treelag_d_1_d_2", "priogrid_month")),'conf_treelag'))
        Datasets.append(FetchTable((Queryset("jim_pgm_conflict_target_sptime_dist_nu1_10_001", "priogrid_month")),'conf_sptime_dist'))

        return(Datasets)


def fetch_pgm_data_from_model_def(qslist):

    level = 'pgm'

    ModelList = ModelDefinitions.DefineEnsembleModels(level)

    defined_querysets=[qs.name for qs in qslist]

    model_querysets=list(set([model['queryset'] for model in ModelList]))

    qs_short_names={}
    for model in ModelList:
        qs_short_names[model['queryset']]=model['data_train']

    Datasets=[]

    for model_qs in model_querysets:
        if model_qs not in defined_querysets:
            raise Exception(f'queryset',model_qs,'is not defined in the imported queryset definitions file')

        Datasets.append(FetchTable((Queryset(model_qs, "country_month")), qs_short_names[model_qs]))

    return Datasets

def get_training_data(Datasets, ModelList, model_name):
    for model in ModelList:
        if model['modelname'] == model_name:
            ds_name = model['data_train']

            for item in Datasets:

                if item['Name'] == ds_name:
                    return item['df']
            else:
                print('dataset not found')
                return None
    else:
        print('model', model_name, 'not found')
        return None


def data_integrity_check(dataset, depvar):
    if depvar not in dataset['df'].columns:
        print(depvar, 'not found in', dataset['Name'])
        return

    if dataset['df'].columns[0] != depvar:
        print('Reordering columns in model', dataset['Name'])
        depvar_column = dataset['df'].pop(depvar)
        dataset['df'].insert(0, depvar, depvar_column)

    if 'country_id' in dataset['df'].columns:
        print('country_id found in dataset for ', dataset['Name'], '- dropping')
        dataset['df'] = dataset['df'].drop(['country_id', ], 1)

    for column in dataset['df'].columns:
        if dataset['df'][column].isna().sum() != 0:
            print('WARNING - NaN/Null data detected in', dataset['Name'], 'column', column)

    return


def index_check(model, df_with_wanted_index):
    level0_name_wanted, level1_name_wanted = df_with_wanted_index.index.names

    for key in model.keys():
        try:
            df_index = model[key].index

            level0_name_have, level1_name_have = df_index.names

            if (level0_name_have != level0_name_wanted) or (level1_name_have != level1_name_wanted):
                print('Repairing index in ', key, 'from', model['modelname'])
                print('original:', level0_name_have, level1_name_have)
                print('fixed:', level0_name_wanted, level1_name_wanted)

                model[key].index.set_names([level0_name_wanted, level1_name_wanted], inplace=True)

        except:
            pass

    return


def PCA(source, Standard_features, EndOfPCAData):
    df = source['dataset'].loc[121:EndOfPCAData].copy()
    df = df.replace([np.inf, -np.inf], 0) 
    df = df.fillna(0)
    pca = decomposition.PCA(n_components=source['n_comp'])
    pca.fit(df)
    df1 = pd.DataFrame(pca.transform(df))

    print(source['name'],pca.explained_variance_ratio_)

    print(pca.singular_values_)
    df2 = source['dataset'][Standard_features].loc[121:EndOfPCAData].copy()
    source['result'] = pd.concat([df2, df1.set_index(df2.index)], axis=1)
    colnames = Standard_features.copy()
    for i in range(source['n_comp']):
        colname = 'pc' + str(i+1)
        colnames.append(colname)
    source['result'].columns = colnames
    source['result'].head()
    return(source)


def find_index(dicts, key, value):
    class Null: pass
    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i
    else:
        raise ValueError('no dict with the key and value combination found')


def RetrieveFromList(Datasets,name):
    return Datasets[find_index(Datasets, 'Name', name)]['df']


def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]


def find_between_brackets(s):
    return (s.split('['))[1].split(']')[0]


def document_queryset(qslist,dev_id):
    ''' Writes a markdown file listing the variables in the querysets passed in the list of querysets '''

    file = open("../Documentation/Querysets.md","w")
    file.write('# Documentation of querysets')
    file.write(dev_id)

    for qs in qslist:
        print('Model: ',qs.name)
        file.write(qs.name)
        ModelMetaData = []
        i = 0
        for var in qs.operations:
            VarMetaData = {
                'Model': qs.name,
                'Included variable name': find_between_brackets(str(var[0])),
                'Database variable name': find_between(str(var[-1]),'name=',' ')
            }
            Transformations = []
            for line in var:
    #            print('line:',line)
                item = str(line) 
                if 'trf' in item:
                    trf = find_between(item,'name=',' ')
    #                print('trf:', trf)
                    if 'util.rename' not in trf:
                        Transformations.append(trf)
    #        print(Transformations)
            VarMetaData['Transformations'] = Transformations
            ModelMetaData.append(VarMetaData)
            i= i + 1
        ModelMetaData_df = pd.DataFrame(ModelMetaData)
        filename = '../Documentation/Model_' + qs.name + '.md'
        ModelMetaData_df.to_markdown(index=False, buf=filename)
        this_qs = ModelMetaData_df.to_markdown(index=False)
        file.write(this_qs)
        file.write('')
    file.close()


def document_ensemble(ModelList, outcome):
    ''' Writes a markdown file listing the models passed in the list of models '''
    
    i = 0
    EnsembleMetaData = []
    for model in ModelList:
        print(i, model['modelname'], model['data_train'])
        ModelMetaData = {
            'Model name': model['modelname'],
            'Description': model['description'],
            'Dependent variable': model['depvar'],
            'Queryset': model['queryset'],
            'Algorithm': str(model['algorithm']).split('(')[0],
            'Long description': model['long_description']
        }
        if model['preprocessing'] == 'pca_it':
            ModelMetaData['PCA'] = 'True'
        else:
            ModelMetaData['PCA'] = 'False'
        
        EnsembleMetaData.append(ModelMetaData)
        i = i + 1
        EnsembleMetaData_df = pd.DataFrame(EnsembleMetaData)
        filename = f'../Documentation/Ensemble_{outcome}.md'
        EnsembleMetaData_df.to_markdown(index=False, buf=filename)

# calibration of pgm predictions using cm predictions:
def calibrate_pg_with_c(df_pgm, df_cm, column, df_pg_id_c_id=None, log_feature=False, super_calibrate=False):
    try:
        assert df_pgm.index.names[0] == 'month_id'
    except AssertionError:
        raise ValueError(f"Expected pgm df to have month_id as 1st index")

    try:
        assert df_pgm.index.names[1] in ['priogrid_gid', 'priogrid_id', 'pg_id']
    except AssertionError:
        raise ValueError(f"Expected pgm df to have one of priogrid_gid, priogrid_id, pg_id as 2nd index")

    try:
        assert df_cm.index.names[0] == 'month_id'
    except AssertionError:
        raise ValueError(f"Expected cm df to have month_id as 1st index")

    try:
        assert df_cm.index.names[1] in ['country_id', 'c_id']
    except AssertionError:
        raise ValueError(f"Expected cm df to have one of country_id, c_id as 2nd index")

    try:
        assert column in df_pgm.columns
    except AssertionError:
        raise ValueError(f"Specified column not in pgm df")

    try:
        assert column in df_cm.columns
    except AssertionError:
        raise ValueError(f"Specified column not in cm df")

    input_months_cm = list(set(df_cm.index.get_level_values(0)))
    input_months_pgm = list(set(df_pgm.index.get_level_values(0)))

    input_months_cm.sort()
    input_months_pgm.sort()

    try:
        assert input_months_cm == input_months_pgm
    except AssertionError:
        raise ValueError(f"Inconsistent months found in input dfs")

    input_countries = list(set(df_cm.index.get_level_values(1)))
    input_pgs = list(set(df_pgm.index.get_level_values(1)))
    input_pgs.sort()

    if df_pg_id_c_id is None:
        print('Fetching pd-month-->country-month df from service')
        df_pg_id_c_id = fetch_df_pg_id_c_id()

    pg_size = len(input_pgs)

    normalised = np.zeros((df_pgm[column].size))

    if log_feature:
        df_to_calib = pd.DataFrame(index=df_pgm.index, columns=[column, ], data=np.exp(df_pgm[column].values) - 1)
        df_calib_from = pd.DataFrame(index=df_cm.index, columns=[column, ], data=np.exp(df_cm[column].values) - 1)
    else:
        df_to_calib = pd.DataFrame(index=df_pgm.index, columns=[column, ], data=df_pgm[column].values)
        df_calib_from = pd.DataFrame(index=df_cm.index, columns=[column, ], data=df_cm[column].values)

    for imonth, month in enumerate(input_months_pgm):

        istart = imonth * pg_size
        iend = istart + pg_size

        normalised_month = np.zeros((pg_size))

        df_data_month_pgm = pd.DataFrame(df_to_calib[column].loc[month])

        values_month_pgm = df_to_calib[column].loc[month].values.reshape(pg_size)

        df_data_month_cm = pd.DataFrame(df_calib_from[column].loc[month])

        map_month = df_pg_id_c_id.loc[month].values.reshape(pg_size)

        input_countries = list(set(df_data_month_cm.index.get_level_values(0)))

        for country in input_countries:
            month_country = df_data_month_cm[column].loc[country]
            mask = (map_month == country)

            nmask = np.count_nonzero(mask)

            pg_sum = np.sum(values_month_pgm[mask])

            value_month_cm = df_calib_from[column].loc[month, country]

            if pg_sum > 0:
                normalisation = value_month_cm / pg_sum * np.ones((nmask))

                normalised_month[mask] = values_month_pgm[mask] * normalisation

        if super_calibrate:
            sum_month_cm = np.sum(df_data_month_cm[column])
            if np.sum(normalised_month) > 0:
                normalisation = sum_month_cm / np.sum(normalised_month)
                normalised_month *= normalisation

        normalised[istart:iend] = normalised_month

    if log_feature:
        normalised = np.log(normalised + 1)

    df_out = pd.DataFrame(index=df_pgm.index, columns=[column, ], data=normalised)

    return df_out


# helper function for pgm-cm calibration, which fetches country-ids for pg-ids
def fetch_df_pg_id_c_id():
    qs = (Queryset("jed_pgm_cm", "priogrid_month")
          .with_column(Column("country_id", from_table="country_month", from_column="country_id")

                       )
          )

    df_pg_id_c_id = qs.publish().fetch()

    return df_pg_id_c_id


class SurrogateMetadata:
    def __init__(self, surrogate_model_list):
        df = surrogate_model_list.copy()
        df = pd.DataFrame([self.__filter_key(i) for i in df])
        df['Modelname'] = df.apply(lambda row: ' '.join(row['Modelname'].split()[1:]), axis=1)
        df['Columns'] = df.apply(lambda row: ', '.join(row['Columns']), axis=1)
        df = df.drop_duplicates()
        self.surrogate_model_list = df

    @staticmethod
    def __filter_key(surrogate_model):
        return {key: surrogate_model[key] for key in ('Modelname','Shortname','Longdescription','Columns')}
    
    def to_markdown(self, path=None):
        return self.surrogate_model_list.to_markdown(buf=path)
    
class EnsembleMetadata:
    def __init__(self, EnsembleList):
        df = EnsembleList.copy()
        df = pd.DataFrame([self.__filter_key(i) for i in df])
        df['modelname'] = df.apply(lambda row: ' '.join(row['modelname'].split()[1:]), axis=1)
        #df['Columns'] = df.apply(lambda row: ', '.join(row['Columns']), axis=1)
        df = df.drop_duplicates()
        self.EnsembleList = df

    @staticmethod
    def __filter_key(EnsembleList):
        return {key: EnsembleList[key] for key in ('modelname','depvar','algorithm', 'Algorithm_text')}
    
    def to_markdown(self, path=None):
        return self.EnsembleList.to_markdown(buf=path)