from Tools.visualization_assetts_fat002_add.config2 import *

Monthly_updates = Mydropbox + 'DataReleases/MonthlyUpdates/master_visualization_output_folder/'
label_version = f'fat002_paper'
master_folder = Monthly_updates + label_version

#new folderpath
def make_folders():
    make_a_folder(master_folder)
    print(f"{user}, folders created")