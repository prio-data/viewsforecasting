from Tools.visualization_assetts_fat002_add.external_imports_all import*

#January 1989 to December 2021
StartOfHistory = 109
EndOfHistory = 504

months_wanted = [505, 493, 481, 469, 457]

#specify how your dropbox connected to main ViEWS folder is called
home = os.path.expanduser("~")
user = os.getlogin()
Mydropbox = home + '/Dropbox (ViEWS)/ViEWS/'

folder_name_label = 'fat002_paper'

def sanity_check():
    print(f"{user}, Start of History is {StartOfHistory}, End of History is {EndOfHistory}")