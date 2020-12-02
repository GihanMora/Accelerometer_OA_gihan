import csv
import pandas as pd
import numpy as np
f = 'F:\\OA_CNN\\Data\\supervised_data\\Actigraph\\numpy_window-3600-overlap-0\\HOA1_2019-05-06_15-00-00_to_2019-05-06_22-00-00_60s_raw_features_test.npy'
X_data = []
Y_data = []

npy = np.load(f, allow_pickle=True)
X_data.append(npy.item().get('segments'))
Y_data.append(npy.item().get('activity_classes'))

print(X_data[0])
print(Y_data[0])
# df = pd.read_csv(f)
#
# print(df.head())