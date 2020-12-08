
#Setting the correct working directory where data files and ANNs are located
setwd('C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh')

#Opening nnet library for using artificial neural networks (ANNs)
library(nnet)

input_foldername <- 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_hip/inputs_for_ANN_hip_2015_feature_set_3/'
output_foldername <- 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_hip/outputs_for_ANN_hip_2015_feature_set_3/'
input_files <- list.files(input_foldername)

for(file in input_files){
  #Loading the file for which you want to predict energy expenditure (EE).  In this file, the column names must match the ones in the example data file or the model will not run.  Features must already be calculated.
  
  EEprediction1<-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
  head(EEprediction1,10)
  #Loading the ANN to be used for EE prediction, for this example the hip accelerometer ANN created using only mean and variance (AGhipANN_FeatureSet2).
  nnet_hip<-load("C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_hip/AGhipANN_FeatureSet3.RData")
  
  #Predicting EE with the loaded ANN
  pred_hip<-predict(get(nnet_hip),EEprediction1)
  
  #Creating a .txt file that displays EE for each 30 second epoch
  # write.table(pred_hip, 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_hip/Hip EE prediction Participant1.txt')
  temp_name <- paste(output_foldername, paste(strsplit(file, '_ANN_input_hip_2015_feature_set_3.txt')[1], "_predicted_hip_EE_2015_feature_set_3.csv", sep=""), sep="")
  write.csv(pred_hip, temp_name)
  print(paste('predicted for hip 2015_feature_set_3 - ', file))
}


# #Loading the file for which you want to predict energy expenditure (EE).  In this file, the column names must match the ones in the example data file or the model will not run.  Features must already be calculated.
# EEprediction1<-read.table(file='C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/Participant 1 example data_FeatureSet2_MSSE 2015 study.txt',header=TRUE)
# 
# #Loading the ANN to be used for EE prediction, for this example the hip accelerometer ANN created using only mean and variance (AGhipANN_FeatureSet2).
# nnet_thigh<-load("C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/AGthighANN_FeatureSet3.RData")
# 
# #Predicting EE with the loaded ANN
# pred_thigh<-predict(get(nnet_thigh),EEprediction1)
# 
# #Creating a .txt file that displays EE for each 30 second epoch
# write.table(pred_thigh, 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/Thigh EE prediction Participant1.txt')

