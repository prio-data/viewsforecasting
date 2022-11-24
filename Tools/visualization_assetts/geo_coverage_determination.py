from Tools.visualization_assetts.external_imports_all import*

def give_me_top_countries(top_number_current, variable_wanted_current, variable_transformation_current):
    
    model_wanted = 'genetic_ensemble'
    dev_id = 'fatalities001'
    run_id = dev_id
    model_attempt = 't01'
    EndOfHistory = 511


    #this will give you the top X country with predicted cumulatie fatalities at cm level for step1 through 36, please make sure that below uses actual and non-transformed value, though should technically still work for ln_variables. order in the list is based on the country numbers, so do not split the list. 
    predstore_future =  'cm_' + model_wanted + '_f' + str(EndOfHistory)

    predictions_df = pd.DataFrame.forecasts.read_store(predstore_future, run=dev_id)

    #Redefine month_id into steps as a index, change the name of some variables for consistency/workability with code
    #note step combined is already a log transformed variable that uses state-based violence
    predictions_df = predictions_df.reset_index()
    predictions_df['step'] = predictions_df['month_id'] - EndOfHistory
    predictions_df = predictions_df.set_index(['step', 'country_id'], drop = True)

    #number of countries wanted to get the top for, note they are not listed from top to low, but rather in numerical order
    #please change in case of changes in the future to the naming convention, otherwise keep as is
    top_wanted = top_number_current
    top_countries= give_me_topX_country_id_cumulative(df=predictions_df, time_index = 'step', number_wanted = top_number_current,
                                               variable = variable_wanted_current, start = 1, end = 36, variable_transformation = variable_transformation_current)
    print(f'{user}, the following are the top {top_wanted} countries for fatalities listed for fatality steps 1 through 36 {top_countries}. list in the order from highest to lowest. ')
    return top_countries