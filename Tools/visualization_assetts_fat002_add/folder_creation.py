from Tools.visualization_assetts_fat002_add.config2 import *

Monthly_updates = Mydropbox + 'DataReleases/SystemUpdates/'
label_version = folder_name_label
master_folder = Monthly_updates + label_version

#new folderpath
def make_folders():
    make_a_folder(master_folder)
    print(f"{user}, folders created")