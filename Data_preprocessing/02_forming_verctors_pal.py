import pandas as pd
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm


def reshape_to_windows(dataframe, window_length, input_cols, target_cols):

    # Setup output column names
    col_names_out = target_cols
    print('out',len(col_names_out))
    for i in range(window_length-1, -1, -1):
        col_names_out.extend(['{}(t-{})'.format(cn, i) for cn in input_cols])
    print('cols',len(col_names_out))
    # Reshape for Windowing

    # print('df',dataframe.shape)
    result_data = []
    for i in range(0, (dataframe.shape[0]-window_length), window_length):

        df_inputs = dataframe.loc[i:(i+window_length-1), input_cols]
        target_0_value = dataframe.at[i+window_length-1, target_cols[0]]
        target_1_value = dataframe.at[i+window_length-1, target_cols[1]]

        data_row = list(list(np.reshape(df_inputs.values, (window_length * len(input_cols), 1)).T)[0])
        # print(len(data_row))
        result_data.append([target_0_value, target_1_value] + data_row)

    # Set the output dataframe
    # print('epos',len(result_data))
    # print('1strow', len(result_data[0]))
    return pd.DataFrame(result_data, columns=col_names_out)



window_length = 300  # 60 seconds (60Hz)


INPUT_DATA_FOLDER = 'F:/OA_CNN/Data/raw_features_pal/'
OUTPUT_FOLDER = join('F:/OA_CNN/Data/', 'supervised_data/ActivPAL/', 'window-{}'.format(window_length))
if not exists(OUTPUT_FOLDER):
    makedirs(OUTPUT_FOLDER)



raw_files = [f for f in listdir(INPUT_DATA_FOLDER) if isfile(join(INPUT_DATA_FOLDER, f))]
# print(raw_files)
for f in tqdm(raw_files):
#     #  84%|████████▎ | 705/842 [5:39:10<1:15:31, 33.08s/it]
    print(f)
    input_cols = ['X', 'Y', 'Z']
    target_cols = ['thigh_EE', 'thigh_intensity_ee_based']
    all_cols = input_cols+target_cols
    df = pd.read_csv(join(INPUT_DATA_FOLDER, f), usecols=all_cols)
    # print(df.head())

    # print('tttt',len(target_cols))
    supervised_data = reshape_to_windows(df, window_length, input_cols, target_cols)

    out_name = join(OUTPUT_FOLDER, f.replace('.csv', '_supervised.csv'))
    supervised_data.to_csv(out_name, index=None)

