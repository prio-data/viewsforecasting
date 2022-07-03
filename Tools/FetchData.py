
from viewser import Queryset, Column
import numpy as np
import pandas as pd
from sklearn import decomposition
from sklearn.decomposition import PCA
import cm_querysets

def ReturnQsList():
    return cm_querysets2.qslist

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
    Data = {
            'Name': name,
            'df': df
        }
    return(Data)

def FetchData(run_id):
    print(f'Fetching data using querysets; {run_id}; returns as list of dictionaries containing datasets')
    Datasets = []

    if run_id == 'Fatalities002':
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
        Datasets.append(FetchTable((Queryset("Fatalities002_faostat", "country_month")),'faostat'))
        Datasets.append(FetchTable((Queryset("Fatalities002_faoprices", "country_month")),'faoprices'))
        Datasets.append(FetchTable((Queryset("Fatalities001_imfweo", "country_month")),'imfweo'))

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

        EndOfPCAData = 516
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

    if run_id == 'Fatalities001':
        Datasets.append(FetchTable((Queryset("hh_fatalities_ged_ln_ultrashort", "country_month")),'baseline'))
        Datasets.append(FetchTable((Queryset("hh_fatalities_ged_acled_ln", "country_month")),'conflictlong_ln'))
        Datasets.append(FetchTable((Queryset("fat_cm_conflict_history", "country_month")),'conflict_ln'))
        Datasets.append(FetchTable((Queryset("fat_cm_conflict_history_exp", "country_month")),'conflict_nolog'))
        Datasets.append(FetchTable((Queryset("hh_fatalities_wdi_short", "country_month")),'wdi_short'))
        Datasets.append(FetchTable((Queryset("hh_fatalities_vdem_short", "country_month")),'vdem_short'))
        Datasets.append(FetchTable((Queryset("hh_topic_model_short", "country_month")),'topics_short'))
        Datasets.append(FetchTable((Queryset("hh_broad", "country_month")),'broad'))
#        Datasets.append(FetchTable((Queryset("hh_prs", "country_month")),'prs'))
        Datasets.append(FetchTable((Queryset("hh_greatest_hits", "country_month")),'gh'))
        Datasets.append(FetchTable((Queryset("hh_20_features", "country_month")),'hh20'))
        Datasets.append(FetchTable((Queryset("hh_all_features", "country_month")),'all_features'))

        # PCA
        Standard_features = ['ln_ged_sb_dep','ln_ged_sb', 'decay_ged_sb_5', 'decay_ged_os_5', 'splag_1_decay_ged_sb_5', 'wdi_sp_pop_totl']

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

        EndOfPCAData = 516
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
        

    return(Datasets)

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

    for qs in cm_querysets2.qslist:
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
        i= i + 1
        EnsembleMetaData_df = pd.DataFrame(EnsembleMetaData)
        filename = f'../Documentation/Ensemble_{outcome}.md'
        EnsembleMetaData_df.to_markdown(index=False, buf=filename)    
 
