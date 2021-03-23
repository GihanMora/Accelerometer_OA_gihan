from os.path import join

import pandas as pd
import statistical_extensions as SE
csv_f = pd.read_csv('E:\Data\Accelerometer_Dataset_Rashmika\OA_data\Hibbing\\new\\entire_df.csv')

# print(csv_f.head())
print(csv_f.columns)

test_Y_data = csv_f['waist_ee'].to_list()
y_pred_test = csv_f['EE_hibbing_corrected'].to_list()

print(test_Y_data)
print('***')
print(y_pred_test)
test_ID_user = []
for i in range(len(test_Y_data)):
    test_ID_user.append(i)

results_df = pd.DataFrame(
    {'subject': test_ID_user,
      'waist_ee': list(test_Y_data),
      'predicted_ee': list(y_pred_test),
'waist_ee_cleaned': list(test_Y_data),
      'predicted_ee_cleaned': list(y_pred_test)
      })

print(results_df['waist_ee'].to_list())

def clean_data_points(data):
    data = data.assign(waist_ee_cleaned=data['waist_ee'].to_list())
    data = data.assign(predicted_ee_cleaned=data['predicted_ee'].to_list())
    data.loc[(data['predicted_ee'] < 1), 'predicted_ee_cleaned'] = 1
    return data

results_df = clean_data_points(results_df)
# print(results_df['waist_ee_cleaned'].to_list())
# print('matrix')
# mean = results_df.as_matrix(columns='waist_ee_cleaned')
# print(mean)
SE.BlandAltman.bland_altman_paired_plot_tested(results_df, 'FOLDER_NAME', 1, log_transformed=True,
                                                min_count_regularise=False, output_filename=join('E:\Projects\Accelerometer_OA_gihan\Evaluating_existing_models\Hibbing\plots', 'bland_altman'))
