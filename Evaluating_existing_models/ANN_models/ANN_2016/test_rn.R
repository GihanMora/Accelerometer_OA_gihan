library(nnet)
library(caret)

nnet_wrist<-load("C:/Users/gihan/Desktop/Montoye/ANN_2016/left_PAintensity.RData")
input_foldername = 'C:/Users/gihan/Desktop/Montoye/ANN_2016/'
file = 'output_lwrist.txt'
EEprediction1<-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
pred_wrist <- predict(get(nnet_wrist),EEprediction1)


nnet_thigh<-load("C:/Users/gihan/Desktop/Montoye/ANN_2016/thigh_PAintensity.RData")
input_foldername = 'C:/Users/gihan/Desktop/Montoye/ANN_2016/'
file = 'output.txt'
EEprediction1<-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
pred_thigh <- predict(get(nnet_thigh),EEprediction1)


nnet_hip<-load("C:/Users/gihan/Desktop/Montoye/ANN_2016/hip_PAintensity.RData")
input_foldername = 'C:/Users/gihan/Desktop/Montoye/ANN_2016/'
file = 'hip_data_2016.txt'
EEprediction1<-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
pred_hip <- predict(get(nnet_hip),EEprediction1)

