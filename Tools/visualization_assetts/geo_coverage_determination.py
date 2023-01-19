from Tools.visualization_assetts.config1 import*

def give_me_top_countries():
    
    predstore_future =  'cm_' + model_wanted + '_f' + str(EndOfHistory)

    predictions_df = pd.DataFrame.forecasts.read_store(predstore_future, run=dev_id)

    #Redefine month_id into steps as a index, change the name of some variables for consistency/workability with code
    #note step combined is already a log transformed variable that uses state-based violence
    predictions_df = predictions_df.reset_index()
    predictions_df['step'] = predictions_df['month_id'] - EndOfHistory
    predictions_df = predictions_df.set_index(['step', 'country_id'], drop = True)

    #number of countries wanted to get the top for
    #please change in case of changes in the future to the naming convention, otherwise keep as is
    top_countries= give_me_topX_country_id_cumulative(df=predictions_df, time_index = 'step', number_wanted = top_wanted,
                                               variable = 'step_combined', start = 1, end = 36, variable_transformation = 'ln1')
    return top_countries

top_countries = give_me_top_countries()


#these are the loops, if you want to ammend them please change the loops below by adding specific country_ids
if more_countries == 'true':
    geo_coverage_loop = ['globe', 'ame', 'africa', *top_countries, country]
    line_chart_region = ['globe', 'ame', 'africa', country]
    bar_chart_region = {'ame', 'africa', tuple(top_countries), country}
    pie_chart_region = {'globe', 'ame', 'africa', tuple(top_countries), country}
if more_countries == 'false':
    geo_coverage_loop = ['globe', 'ame', 'africa', *top_countries]
    line_chart_region = ['globe', 'ame', 'africa']
    bar_chart_region = {'ame', 'africa', tuple(top_countries)}
    pie_chart_region = {'globe', 'ame', 'africa', tuple(top_countries)}


def sanity_check():
    print(f"{user}, you have chosen to model {model_wanted} at cm level and {model_wanted_pgm} at pgm level. The dev_id is {dev_id}, the model attempt is {model_attempt}. the comparison for change models is dev_id {dev_id_comparison}. Your End Of history is {EndOfHistory}")
    print(f'{user}, the following are the top {top_wanted} countries for fatalities listed for fatality steps 1 through 36 {top_countries}. list in the order from highest to lowest. These countries will be part of the global geo_loop')
    print(f"the following geo loops will be included in the current run. for maps geo_coverage_loops is {geo_coverage_loop}, for line graphs the loop is {line_chart_region}, for bar the loop is {bar_chart_region}, and for pie the loop is {pie_chart_region}")
    print(f"{user}, your dropbox views file is this {Mydropbox}")