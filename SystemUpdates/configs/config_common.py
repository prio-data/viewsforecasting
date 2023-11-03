
dev_id = 'Fatalities003'
run_id = 'Fatalities003'
EndOfHistory = 509
RunGeneticAlgo = True
level = 'cm'
get_future = False

username = getpass.getuser()

steps = [*range(1, 36+1, 1)] # Which steps to train and predict for

fi_steps = [1,3,6,12,36]
# Specifying partitions

calib_partitioner_dict = {"train":(121,396),"predict":(397,444)}
test_partitioner_dict = {"train":(121,444),"predict":(445,492)}
future_partitioner_dict = {"train":(121,492),"predict":(493,504)}
calib_partitioner =  views_runs.DataPartitioner({"calib":calib_partitioner_dict})
test_partitioner =  views_runs.DataPartitioner({"test":test_partitioner_dict})
future_partitioner =  views_runs.DataPartitioner({"future":future_partitioner_dict})

Mydropbox = f'/Users/{username}/Dropbox (ViEWS)/ViEWS/'
localpath = f'/Users/{username}/Pickles/'
overleafpath = f'/Users/{username}/Dropbox (ViEWS)/Apps/Overleaf/VIEWS documentation {dev_id}/'