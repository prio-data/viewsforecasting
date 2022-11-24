#importing all the necessary functions
# Basics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText


import warnings
warnings.filterwarnings('ignore')

#Views 3
from viewser.operations import fetch
from viewser import Queryset, Column
#import views_runs

from views_runs import storage, ModelMetadata
from views_runs.storage import store, retrieve, fetch_metadata
from views_forecasts.extensions import *

#Data fetching of predictions, note the rewrite required to make the .py files work from a different folder, may require change if the organization of the main branch changed
import sys
import os
home = os.path.expanduser("~")
user = os.getlogin()

#fix for the Ensembling folder location in comparison to the working directory
#def get_2up_dir(directory):
    #import os
    #return os.path.dirname(os.path.dirname((directory)))  
#viewsforecasting = get_2up_dir(os.getcwd())
#sys.path.append(viewsforecasting+'/Tools')
#sys.path.append(viewsforecasting+'/Intermediates')
#sys.path.append(viewsforecasting+'/SystemUpdates')

#MapperTools
import os
import geopandas as gpd
import sqlalchemy as sa
from ingester3.config import source_db_path
from views_mapper2.mapper2 import *
from views_mapper2.dictionary_writer import *
from views_mapper2.BBoxWriter import *
from views_mapper2.label_writer import *