# Script to set parameters for markov models

qs = "fatalities002_joint_narrow" # Queryset to fetch
save_name = 'jointnarrow' # save name for run
save_path = 'results/'
EndOfHistory = 511 # End of history, only needed for predict_type == 'future'
steps = [*range(1, 36+1, 1)] # Which steps to train and predict for

calib_partitioner_dict = {"train":(121,408),"predict":(409,456)} # Calib partition
test_partitioner_dict = {"train":(121,456),"predict":(457,504)} # Test partition
# custom_partitioner_dict = {"train":(121,456),"predict":(457,504)} # Custom partition to set your own train and predict ranges

model_type = 'both' # Either 'rf', 'glm', or 'both'
predict_type = 'test' # 'future', 'test', 'calib', or 'custom'

cleenup = False # should all temporary files and tmps folder be removed at the end?
