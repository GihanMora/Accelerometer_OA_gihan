import pandas as pd
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
import pickle
import pandas as pd
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
from random import sample
from scipy import stats
import operator

def create_segments_and_labels(df, time_steps, step, n_features, label_class, label_2):

    # class_count_map = {}
    # for i in range(0, len(df) - time_steps, step):
    #     timestep_data = df[label_class][i: i + time_steps]
    #     # If multiple classes in same segment, continue
    #     if len(set(timestep_data)) != 1:
    #         continue
    #     class_count_map[i] = timestep_data.iloc[0]
    #
    # sorted_class_count_map = sorted(class_count_map.items(), key=operator.itemgetter(1), reverse=False)
    # ordered_classes = [i for _, i in sorted_class_count_map]
    # start_point = len(ordered_classes) - 2 * (len(ordered_classes) - ordered_classes.index(2))
    # filtered_tuples = sorted_class_count_map[start_point:]

    # Down Sampling - Manual approach to solve data imbalance problem
    lmvpa_begin_class = 2
    class_count_map = {}
    for i in range(0, len(df) - time_steps, step):
        timestep_data = df[label_class][i: i + time_steps]
        # If multiple classes in same segment, continue
        if len(set(timestep_data)) != 1:
            continue
        class_count_map[i] = timestep_data.iloc[0]

    sorted_class_count_map = sorted(class_count_map.items(), key=operator.itemgetter(1), reverse=False)
    print('sorted_class_count_map',sorted_class_count_map)

    ordered_classes = [i for _, i in sorted_class_count_map]
    print('ordered_classes',ordered_classes)

    divide_index = ordered_classes.index(lmvpa_begin_class)
    print('divide_index',divide_index)

    lmvpa = sorted_class_count_map[divide_index:]
    print('lmvpa',lmvpa)
    sb = sample(sorted_class_count_map[:divide_index], len(lmvpa)) if divide_index > len(lmvpa) else sorted_class_count_map[:divide_index]
    print('sb',sb)

    filtered_tuples = sb + lmvpa

    segments = []
    labels = []
    regression_values = []
    for i, c in filtered_tuples:
        xs = df['X'].values[i: i + time_steps]
        ys = df['Y'].values[i: i + time_steps]
        zs = df['Z'].values[i: i + time_steps]
        # Retrieve the most often used label in this segment
        class_label = c
        class_reg = df[label_2][i: i + time_steps].mean()
        segments.append([xs, ys, zs])
        labels.append(class_label)
        regression_values.append(class_reg)

    # Bring the segments into a better shape
    reshaped_segments = np.asarray(segments, dtype=np.float32).reshape(-1, time_steps, n_features)
    labels = np.asarray(labels)
    regression_values = np.asarray(regression_values)

    return {'segments': reshaped_segments, 'activity_classes': labels, 'energy_e': regression_values}


time_window = 3600
N_FEATURES = 3
LABEL_CLASS = 'waist_intensity_ee_based'
LABEL_REG = 'waist_ee'
req_cols = ['X', 'Y', 'Z', 'waist_ee', 'waist_intensity_ee_based']
input_cols = ['X', 'Y', 'Z']
target_cols = ['waist_ee', 'waist_intensity_ee_based']


INPUT_DATA_FOLDER = 'E:/Data/Accelerometer_Dataset_Rashmika/OA_data/raw_features_graph/'
OUTPUT_FOLDER_ROOT = join('E:/Data/Accelerometer_Dataset_Rashmika/OA_data/', 'supervised_data/ActivGraph/balanced/')
if not exists(OUTPUT_FOLDER_ROOT):
    makedirs(OUTPUT_FOLDER_ROOT)


fss=open('errors.txt','a+')
raw_files = [f for f in listdir(INPUT_DATA_FOLDER) if isfile(join(INPUT_DATA_FOLDER, f))]
for f in tqdm(raw_files):
#     #  84%|████████▎ | 705/842 [5:39:10<1:15:31, 33.08s/it]
    print(f)
    df = pd.read_csv(join(INPUT_DATA_FOLDER, f), usecols=req_cols)
    STEP_DISTANCE = time_window
    try:
        reshaped_outcomes = create_segments_and_labels(df, time_window, STEP_DISTANCE,
                                               N_FEATURES, LABEL_CLASS, LABEL_REG)
    except Exception as e:
        fss.write(f+'\n')

    OUTPUT_FOLDER = join(OUTPUT_FOLDER_ROOT, 'numpy_window-{}-overlap-{}'.format(time_window, int(0)))
    if not exists(OUTPUT_FOLDER):
                        makedirs(OUTPUT_FOLDER)
    out_name = join(OUTPUT_FOLDER, f.replace('.csv', '_test.npy'))
    np.save(out_name, reshaped_outcomes)

fss.close()
