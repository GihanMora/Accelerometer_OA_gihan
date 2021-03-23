
from os import listdir
from os.path import isfile, join

epoch_path = "E:\Data\Accelerometer_Dataset_Rashmika\OA_data\Hibbing\\new\Epoch1\\"

combined_results_folder = epoch_path
combined_data_files = [f for f in listdir(combined_results_folder) if isfile(join(combined_results_folder, f))]
combined_ids = [f.split('_')[0] for f in listdir(combined_results_folder) if isfile(join(combined_results_folder, f))]
combined_ids = list(set(combined_ids))
# results_file = evaluation_results_hip+'caron_hip.csv'

print(combined_ids)


import csv
import pandas as pd
def met_to_intensity_ground_cm_hibbing(row):
  ee = combined_data['waist_ee'][row.name]
  return 1 if ee <= 1.5 else 2 if ee < 3 else 3

def met_to_intensity_hibbing(row):
  ee = combined_data['EE_hibbing_corrected'][row.name]
  return 1 if ee <= 1.5 else 2 if ee < 3 else 3

entire_df = pd.DataFrame()

for each_id in combined_ids:
  complete_df = pd.DataFrame()
  # print(combined_data_files)
  for combined_file in combined_data_files:
    if(combined_file.split('_')[0] != each_id):continue
    combined_data = pd.read_csv(combined_results_folder + combined_file)
    ground_truths = combined_data['waist_ee']
    ground_intensity = combined_data.apply(met_to_intensity_ground_cm_hibbing,axis=1)
    predictions_hip = combined_data['EE_hibbing_corrected']
    predicted_intensity = combined_data.apply(met_to_intensity_hibbing,axis=1)


    combined_data['ground_intensity'] = ground_intensity
    combined_data['predicted_intensity'] = predicted_intensity

    #concatenating each file of one patient
    complete_df = pd.concat([complete_df,combined_data])
  # print(complete_df.head())
  entire_df = pd.concat([entire_df, complete_df])
  


entire_df.to_csv('E:\Data\Accelerometer_Dataset_Rashmika\OA_data\Hibbing\\new\\entire_df.csv')