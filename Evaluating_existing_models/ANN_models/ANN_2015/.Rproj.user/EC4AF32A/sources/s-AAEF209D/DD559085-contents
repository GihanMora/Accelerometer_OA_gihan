library(nnet)
library(caret)

#wrist
nnet_wrist<-load("C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/left_PAintensity.RData")
input_foldername = 'C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/'
file = 'wrist_sample.txt'
EEprediction1<-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
pred_wrist <- predict(get(nnet_wrist),EEprediction1)

#Creating a .txt file that displays EE for each 30 second epoch
write.table(pred_wrist, 'C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/sample_output_wrist.txt')




#thigh
nnet_thigh<-load("C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/thigh_PAintensity.RData")
input_foldername = 'C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/'
file = 'thigh_sample.txt'
thigh_input <-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
pred_thigh <- predict(get(nnet_thigh),thigh_input)


#Creating a .txt file that displays EE for each 30 second epoch
write.table(pred_thigh, 'C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/sample_output_thigh.txt')




#hip
nnet_hip<-load("C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/hip_PAintensity.RData")
input_foldername = 'C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/'
file = 'hip_sample.txt'
hip_input <-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
pred_hip <- predict(get(nnet_hip),hip_input)

#Creating a .txt file that displays EE for each 30 second epoch
write.table(pred_thigh, 'C:/Users/gihan/Desktop/Montoye/ANN_2016/ANN_2016/sample_output_hip.txt')

