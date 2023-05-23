from Tools.visualization_assetts.config2 import *

Monthly_updates = Mydropbox + 'DataReleases/MonthlyUpdates/'
label_version = f'{dev_id}_{model_wanted}_{vid2date_version2(EndOfHistory+1)}_{model_attempt}'
master_folder = Monthly_updates + label_version

#new folderpath
def make_folders():
    make_folders_complete_set(master_folder)
    print(f"{user}, folders created")