import pandas as pd
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
import pickle


def create_segments_and_labels(dataframe, time_steps, step, n_features, label_class, label_2):

    segments = []
    labels = []
    regression_values = []
    for i in range(0, len(dataframe) - time_steps, step):
        xs = dataframe['X'].values[i: i + time_steps]
        ys = dataframe['Y'].values[i: i + time_steps]
        zs = dataframe['Z'].values[i: i + time_steps]
        # print(xs)
        # print(ys)
        # print(zs)
        # Retrieve the most often used label in this segment
        class_label = dataframe[label_class][i: i + time_steps].mode()[0]
        class_reg = dataframe[label_2][i: i + time_steps].mean()
        segments.append([xs, ys, zs])
        # print(segments)
        labels.append(class_label)
        regression_values.append(class_reg)


    # Bring the segments into a better shape
    reshaped_segments = np.asarray(segments, dtype=np.float32).reshape(-1, time_steps, n_features)
    # print(reshaped_segments)
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


INPUT_DATA_FOLDER = 'F:/OA_CNN/Data/raw_features_graph/'
OUTPUT_FOLDER_ROOT = join('F:/OA_CNN/Data/', 'supervised_data/Actigraph/')
if not exists(OUTPUT_FOLDER_ROOT):
    makedirs(OUTPUT_FOLDER_ROOT)



raw_files = [f for f in listdir(INPUT_DATA_FOLDER) if isfile(join(INPUT_DATA_FOLDER, f))]
for f in tqdm(raw_files):
#     #  84%|████████▎ | 705/842 [5:39:10<1:15:31, 33.08s/it]
    print(f)
    df = pd.read_csv(join(INPUT_DATA_FOLDER, f), usecols=req_cols)
    STEP_DISTANCE = time_window
    reshaped_outcomes = create_segments_and_labels(df, time_window, STEP_DISTANCE,
                                               N_FEATURES, LABEL_CLASS, LABEL_REG)
    OUTPUT_FOLDER = join(OUTPUT_FOLDER_ROOT, 'numpy_window-{}-overlap-{}'.format(time_window, int(0)))
    if not exists(OUTPUT_FOLDER):
                        makedirs(OUTPUT_FOLDER)
    out_name = join(OUTPUT_FOLDER, f.replace('.csv', '_test.npy'))
    np.save(out_name, reshaped_outcomes)
