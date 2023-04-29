from Tools.visualization_assetts_fat002_add.external_imports_all import*

#January 1989 to December 2022
StartOfHistory = 109
EndOfHistory = 516

months_wanted = [505, 493, 481, 469, 457]

#specify how your dropbox connected to main ViEWS folder is called
home = os.path.expanduser("~")
user = os.getlogin()
Mydropbox = home + '/Dropbox (ViEWS)/ViEWS/'