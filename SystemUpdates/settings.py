import views_runs
import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.append(parent_dir)

# Add the 'Tools' subdirectory of the parent directory to the system path
sys.path.append(os.path.join(parent_dir, 'Tools'))

# Add the 'Intermediates' subdirectory of the parent directory to the system path
sys.path.append(os.path.join(parent_dir, 'Intermediates'))

LEVEL = 'cm'

DEV_ID = 'Fatalities003'
RUN_ID = DEV_ID
username = os.getlogin()
Mydropbox = f'/Users/{username}/Dropbox (ViEWS)/ViEWS'
overleafpath = f'/Users/{username}/Dropbox (ViEWS)/Apps/Overleaf/VIEWS documentation {DEV_ID}/'

RerunQuerysets = True
FutureStart = 508
steps = [*range(1, 36+1, 1)] # Which steps to train and predict for
fi_steps = [1,3,6,12,36] # Which steps to present feature importances for
calib_partitioner_dict = {"train":(121,396),
                          "predict":(397,444)}
calib_partitioner =  views_runs.DataPartitioner({"calib":calib_partitioner_dict})

test_partitioner_dict = {"train":(121,444),
                         "predict":(445,492)}
test_partitioner =  views_runs.DataPartitioner({"test":test_partitioner_dict})

future_partitioner_dict = {"train":(121,492),
                           "predict":(493,504)}
future_partitioner =  views_runs.DataPartitioner({"future":future_partitioner_dict})
