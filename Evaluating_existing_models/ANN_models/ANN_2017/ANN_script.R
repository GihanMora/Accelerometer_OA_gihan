
#Setting the correct working directory where data files and ANNs are located
setwd('C:/Users/gihan/Desktop/Montoye/ANN_2017')

#Opening nnet library for using artificial neural networks (ANNs)
library(nnet)

#Loading the file for which you want to predict energy expenditure (EE).  In this file, the column names must match the ones in the example data file or the model will not run.  Features must already be calculated.
EEprediction1<-read.table(file='C:/Users/gihan/Desktop/Montoye/ANN_2017/sample_data_input.txt',header=TRUE)

#Loading the ANN to be used for EE prediction, for this example the activPAL thigh-worn accelerometer ANN created using only mean and variance (APthighANN_FeatureSet2).
nnet_activPAL<-load("C:/Users/gihan/Desktop/Montoye/ANN_2017/APthighANN_FeatureSet2.RData")

#Predicting EE with the loaded ANN
pred_activPAL<-predict(get(nnet_activPAL),EEprediction1)

#Creating a .txt file that displays EE for each 30 second epoch
write.table(pred_activPAL, 'C:/Users/gihan/Desktop/Montoye/ANN_2017/sample_prediction.txt')



