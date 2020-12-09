# -*- coding: utf-8 -*-
"""CNN_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eyc--ceh4kX8_eYdBJ_o-yqFlAiwZrrf
"""



from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from os import listdir, makedirs
from os.path import join, isfile, exists
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import shutil
from tqdm import tqdm
from time import time
import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Reshape, GlobalMaxPooling1D
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
# tboard_log_dir = os.path.join("logs",'mylog')
# tensorboard = TensorBoard(log_dir = tboard_log_dir)
from scipy.stats.stats import pearsonr
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score, confusion_matrix

import statistical_extensions as SE

training_dataset_path = 'E:/Data/Accelerometer_Dataset_Rashmika/OA_data/supervised_data/ActivPAL/numpy_window-300-overlap-150_train/'
test_dataset_path = 'E:/Data/Accelerometer_Dataset_Rashmika/OA_data/supervised_data/ActivPAL/numpy_window-300-overlap-150_test/'
temp_model_out_folder = 'E:/Projects/Accelerometer_OA_gihan/CNN_ACCL_OA/Model_outputs/CNN_pal_reg/temp_model_out/'
MODEL_FOLDER = 'E:/Projects/Accelerometer_OA_gihan/CNN_ACCL_OA/Model_outputs/CNN_pal_reg/'
TIME_PERIODS = 300
model_checkpoint_path = 'E:/Projects/Accelerometer_OA_gihan/CNN_ACCL_OA/Model_outputs/CNN_pal_reg/temp_model_out/'

def load_data(filenames):

    X_data = []
    Y_data = []
    ID_user = []
    counter = 0
    for filename in tqdm(filenames):
        npy = np.load(filename, allow_pickle=True)
        X_data.append(npy.item().get('segments'))
        Y_data.append(npy.item().get('energy_e'))

        user_id = filename.split('/')[-1][:6]
        data_length = npy.item().get('energy_e').shape[0]
        ID_user.extend([user_id for _ in range(data_length)])

        # counter += 1
        # if counter > 10:
        #     break

    X_data = np.concatenate(X_data, axis=0)
    Y_data = np.concatenate(Y_data, axis=0)

    return X_data, Y_data, ID_user

# f = '/content/drive/My Drive/CNN/HOA10_2019-06-24_14-00-00_to_2019-06-24_21-00-00_60s_raw_features_test.npy'
#
# x,y,id = load_data([f])
# print(x.shape)
# print(x[0])

def plot_model(history, MODEL_FOLDER):
    # summarize history for accuracy and loss
    plt.figure(figsize=(6, 4))
    plt.plot(history.history['acc'], "g--", label="Accuracy of training data")
    plt.plot(history.history['val_acc'], "g", label="Accuracy of validation data")
    plt.plot(history.history['loss'], "r--", label="Loss of training data")
    plt.plot(history.history['val_loss'], "r", label="Loss of validation data")
    plt.title('Model Accuracy and Loss')
    plt.ylabel('Accuracy and Loss')
    plt.xlabel('Training Epoch')
    plt.ylim(0)
    plt.legend()
    plt.savefig(MODEL_FOLDER + 'learning_history.png')
    plt.clf()
    plt.close()
# print('hi')
#
# training_data_files = [join(training_dataset_path, f) for f in listdir(training_dataset_path) if isfile(join(training_dataset_path, f))]
#
# print(training_data_files)
# train_X_data, train_Y_data, train_ID_user = load_data(training_data_files)
# X_train, y_train, ID_train = train_X_data, train_Y_data, train_ID_user
# # # Data -> Model ready
# print('first',(X_train.shape))
# num_time_periods, num_sensors = X_train.shape[1], X_train.shape[2]
#
# # Set input_shape / reshape for Keras
# input_shape = (num_time_periods * num_sensors)
# X_train = X_train.reshape(X_train.shape[0], input_shape)
#
# # Convert type for Keras otherwise Keras cannot process the data
# X_train = X_train.astype("float32")
# y_train = y_train.astype("float32")
#
#
#

#
#
#
#
# """Model architecture"""
# model_m = Sequential()
# model_m.add(Reshape((TIME_PERIODS, num_sensors), input_shape=(input_shape,)))
# model_m.add(Conv1D(80, 10, activation='relu', input_shape=(TIME_PERIODS, num_sensors)))
# model_m.add(Conv1D(100, 10, activation='relu'))
# model_m.add(MaxPooling1D(3))
# model_m.add(Conv1D(160, 10, activation='relu'))
# model_m.add(Conv1D(180, 10, activation='relu'))
# model_m.add(MaxPooling1D(3))
# model_m.add(Conv1D(220, 10, activation='relu'))
# model_m.add(Conv1D(240, 10, activation='relu'))
# model_m.add(GlobalMaxPooling1D())
# model_m.add(Dropout(0.5))
# model_m.add(Dense(1, activation='linear'))
# print(model_m.summary)
# callbacks_list = [
#     ModelCheckpoint(
#         filepath=model_checkpoint_path+'/best_model.{epoch:03d}-{val_loss:.2f}.h5',
#         monitor='val_loss', save_best_only=True),
#     TensorBoard(log_dir='logs\\{}'.format(time())),
#     EarlyStopping(monitor='val_loss', patience=6)
# ]
#
# model_m.compile(loss='mean_squared_error',
#                 optimizer='adam',
#                 metrics=['accuracy'])
#
# # Hyper-parameters
# BATCH_SIZE = 32
# EPOCHS = 10
#
# history = model_m.fit(X_train,
#                       y_train,
#                       batch_size=BATCH_SIZE,
#                       epochs=EPOCHS,
#                       callbacks=callbacks_list,
#                       validation_split=0.2,
#                       verbose=2)
# _, accuracy = model_m.evaluate(X_train, y_train, batch_size=BATCH_SIZE, verbose=2)
# print(accuracy)
# plot_model(history, MODEL_FOLDER)
#




#prediction part
num_classes = 3
input_shape = 900
model_m =  load_model(join(temp_model_out_folder, 'best_model.010-0.15.h5'))
test_data_files = [join(test_dataset_path, f) for f in listdir(test_dataset_path) if isfile(join(test_dataset_path, f))]
print(test_data_files)
test_X_data, test_Y_data, test_ID_user = load_data(test_data_files)
test_X_data = test_X_data.reshape(test_X_data.shape[0], input_shape).astype("float32")

print('first',test_X_data.shape)
# test_X_data = test_X_data.astype("float32")
test_Y_data = test_Y_data.astype("float32")
# print('Selecting best model.')
#
# model_files = [(join(temp_model_out_folder, f), int(f.split('-')[0].split('.')[1])) for f in
#                listdir(temp_model_out_folder) if
#                isfile(join(temp_model_out_folder, f)) and f.split('-')[0].split('.')[0] != 'final']
#
# model_b_name = sorted(model_files, key=lambda x: x[1], reverse=True)[0][0]
#
# model_b = load_model(model_b_name)
# model_b.save(join(MODEL_FOLDER, model_b_name.split('\\')[1]))
# shutil.rmtree(temp_model_out_folder)
# print('Model Evaluation for {}'.format(grp))
y_pred_test = model_m.predict(test_X_data)
# out_csv= pd.DataFrame()
# out_csv['pred'] = y_pred_test
# out_csv['g_truth'] = test_Y_data
plt.figure(figsize=(8, 8))
plt.scatter(test_Y_data, y_pred_test)
plt.xlabel('Actual EE')
plt.ylabel('Predicted EE')
plt.savefig(join(MODEL_FOLDER, 'actual_vs_predicted_met.png'))
plt.clf()
plt.close()
out_csv= pd.DataFrame()
# print(y_pred_test)
# print(test_Y_data)
# # out_csv['pred'] = y_pred_test
# out_csv['g_truth'] = test_Y_data
# out_csv.to_csv(join('/content/drive/My Drive/CNN/Model_outputs', 'actual_vs_predicted_met.csv'))
y_pred_test_1d_list = [list(i)[0] for i in list(y_pred_test)]
corr = pearsonr(list(test_Y_data), y_pred_test_1d_list)
grp_results = []
grp_results.append('\n\n -------RESULTS-------\n\n')
grp_results.append('Pearsons Correlation = {}'.format(corr))
grp_results.append('RMSE - {}'.format(np.sqrt(mean_squared_error(test_Y_data, y_pred_test))))
grp_results.append('R2 Error - {}'.format(r2_score(test_Y_data, y_pred_test)))
grp_results.append('Explained Variance Score - {}'.format(explained_variance_score(test_Y_data, y_pred_test)))

class_names = ['SED', 'LPA', 'MVPA']
y_test_ai = SE.EnergyTransform.met_to_intensity(test_Y_data)
y_pred_test_ai = SE.EnergyTransform.met_to_intensity(y_pred_test)

cnf_matrix = confusion_matrix(y_test_ai, y_pred_test_ai)

stats = SE.GeneralStats.evaluation_statistics(cnf_matrix)

assessment_result = 'Classes' + '\t' + str(class_names) + '\t' + '\n'
assessment_result += 'Accuracy' + '\t' + str(stats['accuracy']) + '\t' + str(stats['accuracy_ci']) + '\n'
assessment_result += 'Sensitivity' + '\t' + str(stats['sensitivity']) + '\n'
assessment_result += 'Sensitivity CI' + '\t' + str(stats['sensitivity_ci']) + '\n'
assessment_result += 'Specificity' + '\t' + str(stats['specificity']) + '\n'
assessment_result += 'Specificity CI' + '\t' + str(stats['specificity_ci']) + '\n'

grp_results.append(assessment_result)

SE.GeneralStats.plot_confusion_matrix(cnf_matrix, classes=class_names, title='CM',
                                      output_filename=join(MODEL_FOLDER, 'confusion_matrix.png'))


result_string = '\n'.join(grp_results)
with open(MODEL_FOLDER+'/result_report.txt', "w") as text_file:
    text_file.write(result_string)


results_df = pd.DataFrame(
    {'subject': test_ID_user,
      'waist_ee': list(test_Y_data),
      'predicted_ee': [list(i)[0] for i in list(y_pred_test)]
      })

def clean_data_points(data):
    data = data.assign(waist_ee_cleaned=data['waist_ee'])
    data = data.assign(predicted_ee_cleaned=data['predicted_ee'])
    data.loc[(data['predicted_ee'] < 1), 'predicted_ee_cleaned'] = 1
    return data

results_df = clean_data_points(results_df)
# result_string = '\n'.join(grp_results)
# with open(MODEL_FOLDER+'/result_report.txt', "w") as text_file:
#     text_file.write(result_string)

# import statistical_extensions_1 as SE1
SE.BlandAltman.bland_altman_paired_plot_tested(results_df, 'FOLDER_NAME', 1, log_transformed=True,
                                                min_count_regularise=False, output_filename=join(MODEL_FOLDER, 'bland_altman'))

