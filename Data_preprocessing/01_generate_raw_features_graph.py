import os
from os import listdir, makedirs
from os.path import join, isfile, isdir, exists
from datetime import datetime
import pandas as pd
import numpy as np
import math
from tqdm import tqdm


# Input

epoch_folder = 'F:/OA_CNN/Data/Reference_n_bands/actigraph/'
raw_folder = 'F:/OA_CNN/Data/ActiGraph_raw/'

# sleep time input_data
sleep_time_file = 'F:/OA_CNN/Data/metadata/Copy of record_availability_final.csv'

# Output
output_folder = 'F:/OA_CNN/Data/raw_features_graph/'

sleep_df = pd.read_csv(sleep_time_file)
raw_files = [f for f in listdir(raw_folder) if isfile(join(raw_folder, f))]
epoch_files = [f for f in listdir(epoch_folder) if isfile(join(epoch_folder, f))]

data_dict = {f.split()[0]: {'raw': join(raw_folder, f)} for f in raw_files}
for ef in epoch_files:
  key = ef.split()[0]
  if key in data_dict.keys():
    data_dict[key]['epoch'] = join(epoch_folder, ef)

FREQUENCY = 60 #HZ amount of accelerometer
REFERENCE_EPOCH = 60 #Epoch value that EE is given
TIME_EPOCH_DICT = {
    # 'Epoch1': FREQUENCY * 1,
    # 'Epoch5': FREQUENCY * 5,
    # 'Epoch30': FREQUENCY * 30,
    'Epoch60': FREQUENCY * 60
}
print(data_dict)

for _, row in tqdm(sleep_df.iterrows(), total=sleep_df.shape[0]):
    user_id = row['Participant']
    print(_, user_id)
    try:
        begin_time = row['begin_time']
        end_time = row['end_time']

        print(user_id)

        # get respective epoch dataset
        epoch_df = pd.read_csv(data_dict[user_id]['epoch'])
        epoch_df = epoch_df[(begin_time < epoch_df['Time_stamp']) & (epoch_df['Time_stamp'] < end_time)]
        # print(list(epoch_df.index)[0])
        # continue
        # get respective raw dataset
        raw_begin_index = list(epoch_df.index)[0] * REFERENCE_EPOCH * FREQUENCY
        raw_data_length = epoch_df.shape[0] * REFERENCE_EPOCH * FREQUENCY
        raw_df_orig = pd.read_csv(data_dict[user_id]['raw'], skiprows=11 + raw_begin_index, nrows=raw_data_length,
                                  header=None)
        raw_df_orig.columns = ['Timestamp', 'X', 'Y', 'Z']

        del raw_df_orig['Timestamp']
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
                                '{}_{}_to_{}_{}_raw_features.csv'.format(user_id, begin_time, end_time, '60s').replace(':',
                                                                                                               '-').replace(
                                    ' ', '_'))

        merge_data.to_csv(output_file_name, sep=',', index=None)
        # print(merge_data[3595:3605])
        # break

    except Exception as e:
        f = open('errors_graph.txt', 'a+')
        f.write(str(user_id) + " " + str(e) + " \n")
        f.close()