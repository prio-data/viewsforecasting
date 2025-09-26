from Tools.visualization_assetts.external_imports_all import*
#choose the global end of history
#ensure that the choices you are making exist wihtin the internal storage
EndOfHistory = 538

#which model do you want to be graphed within this notebook (accepts one model only)
#if you want a different model, rerun this entire notebook again with that new name
#note that this will produce a separate folder, so should not be an issue
model_wanted = 'genetic_ensemble'
model_wanted_pgm = 'ensemble_cm_calib'

#current month run description
dev_id = 'fatalities002'
run_id = dev_id
model_attempt = 't01'

#comparison run and month
#ensure that the dev_id you are using has information for EndOfHistory-1 month
dev_id_comparison = 'fatalities002'
run_id_comparison = dev_id_comparison
model_wanted_comparison = 'genetic_ensemble'
model_attempt_comparison = 't01'
model_wanted_comparison_pgm = 'ensemble_cm_calib'


#how many top countries do you want to include in the run for all maps
top_wanted = 1

#do you want to include specific countries, write true or false if not, write true and specify countries as a list below, e.g. country = (79,80)
more_countries = True
country = (245,218, 124)


#specify how your dropbox connected to main ViEWS folder is called
home = os.path.expanduser("~")
user = os.getlogin()
Mydropbox = home + '/ViEWS Dropbox/ViEWS/'