from views_runs import ModelMetadata 
from settings import LEVEL

from ModelDefinitions import DefineEnsembleModels

ModelList = DefineEnsembleModels(level=LEVEL)
    
for imodel, model in enumerate(ModelList):
    print(imodel, model['modelname'], model['data_train'])