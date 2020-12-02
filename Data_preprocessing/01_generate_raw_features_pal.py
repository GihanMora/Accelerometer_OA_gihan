import os
from os import listdir, makedirs
from os.path import join, isfile, isdir, exists
from datetime import datetime
import pandas as pd
import numpy as np
import math
from tqdm import tqdm


# Input

epoch_folder = 'F:/OA_CNN/Data/Reference_n_bands/activpal/'
raw_folder = 'F:/OA_CNN/Data/activPAL_raw/'

# sleep time input_data
sleep_time_file = 'F:/OA_CNN/Data/metadata/record_availability_final_pal.csv'

# Output
output_folder = 'F:/OA_CNN/Data/raw_features_pal/'

sleep_df = pd.read_csv(sleep_time_file)
raw_files = [f for f in listdir(raw_folder) if isfile(join(raw_folder, f))]
epoch_files = [f for f in listdir(epoch_folder) if isfile(join(epoch_folder, f))]

data_dict = {f.split('-')[0]: {'raw': join(raw_folder, f)} for f in raw_files}
for ef in epoch_files:
  key = ef.split('-')[0]
  if key in data_dict.keys():
    data_dict[key]['epoch'] = join(epoch_folder, ef)

FREQUENCY = 20 #HZ amount of the accelerometer
REFERENCE_EPOCH = 15 #Epoch value that EE is given
TIME_EPOCH_DICT = {
    # 'Epoch1': FREQUENCY * 1,
    # 'Epoch5': FREQUENCY * 5,
    'Epoch15': FREQUENCY * 15,
    # 'Epoch60': FREQUENCY * 60
}
print(data_dict)

for _, row in tqdm(sleep_df.iterrows(), total=sleep_df.shape[0]):
    user_id = row['Participant']
    print(_, user_id)
    try:
        begin_time = row['begin_time_pal']
        end_time = row['end_time_pal']

        print(user_id)

        # get respective epoch dataset
        epoch_df = pd.read_csv(data_dict[user_id]['epoch'])
        epoch_df = epoch_df[(begin_time < epoch_df['Time_stamp']) & (epoch_df['Time_stamp'] < end_time)]
        # print(list(epoch_df.index)[0])
        # continue
        # get respective raw dataset
        raw_begin_index = list(epoch_df.index)[0] * REFERENCE_EPOCH * FREQUENCY
        raw_data_length = epoch_df.shape[0] * REFERENCE_EPOCH * FREQUENCY

        raw_df_orig = pd.read_csv(data_dict[user_id]['raw'], skiprows=raw_begin_index, sep=';', nrows=raw_data_length,
                                  usecols=[0, 2, 3, 4], header=None)
        raw_df_orig.columns = ['Timestamp', 'X_o', 'Y_o', 'Z_o']

        raw_df_orig['X'] = 0.0157723997930183 * raw_df_orig['X_o'] - 2.01571269354774
        raw_df_orig['Y'] = 0.0157723997930183 * raw_df_orig['Y_o'] - 2.01571269354774
        raw_df_orig['Z'] = 0.0157723997930183 * raw_df_orig['Z_o'] - 2.01571269354774
        del raw_df_orig['Timestamp']
        del raw_df_orig['X_o']
        del raw_df_orig['Y_o']
        del raw_df_orig['Z_o']
        # print(raw_df_orig.head())



        # print(raw_df_orig)

        raw_df_orig.reset_index(inplace=True)

        del epoch_df['Time_stamp']

        n = REFERENCE_EPOCH * FREQUENCY
        print(n)

        epoch_data_repeated = pd.concat([epoch_df] * n).sort_index().reset_index()
        # print(epoch_data_repeated)
        del epoch_data_repeated['index']

        if epoch_data_repeated.shape[0] == raw_df_orig.shape[0]:
            print('OK')
        merge_data = raw_df_orig.merge(epoch_data_repeated, left_index=True, right_index=True)

        del merge_data['index']

        # Save file
        output_file_name = join(output_folder,
                                '{}_{}_to_{}_{}_raw_features.csv'.format(user_id, begin_time, end_time, '15s').replace(':','-').replace(' ', '_'))

        merge_data.to_csv(output_file_name, sep=',', index=None)
        # print(merge_data[3595:3605])
    


    except Exception as e:
        f = open('errors_pal.txt', 'a+')
        f.write(str(user_id) + " " + str(e) + " \n")
        f.close()