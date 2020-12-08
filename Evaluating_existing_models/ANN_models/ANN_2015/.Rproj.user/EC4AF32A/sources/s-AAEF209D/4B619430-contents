
#Setting the correct working directory where data files and ANNs are located
setwd('C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh')

#Opening nnet library for using artificial neural networks (ANNs)
library(nnet)

input_foldername <- 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/inputs_for_ANN_thigh_2015_feature_set_3/'
output_foldername <- 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/outputs_for_ANN_thigh_2015_feature_set_3/'
input_files <- list.files(input_foldername)

# EEprediction1<-read.table(file='C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/inputs_for_ANN_thigh_2015_feature_set_3/HOA1_2019-05-06_14-59-46_to_2019-05-06_22-00-00_Epoch30_ANN_input_thigh_2015_feature_set_3.txt', header=TRUE)
# head(EEprediction1,10)

for(file in input_files){
  #Loading the file for which you want to predict energy expenditure (EE).  In this file, the column names must match the ones in the example data file or the model will not run.  Features must already be calculated.

  EEprediction1<-read.table(file=paste(input_foldername, file, sep=""), header=TRUE)
  head(EEprediction1,10)
  #Loading the ANN to be used for EE prediction, for this example the hip accelerometer ANN created using only mean and variance (AGhipANN_FeatureSet2).
  nnet_thigh<-load("C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_thigh/AGthighANN_FeatureSet3.RData")

  #Predicting EE with the loaded ANN
  pred_thigh<-predict(get(nnet_thigh),EEprediction1)

  #Creating a .txt file that displays EE for each 30 second epoch
  # write.table(pred_hip, 'C:/Users/gihan/Desktop/Montoye/ANN_2015/features_set_3_hip/Hip EE prediction Participant1.txt')
  temp_name <- paste(output_foldername, paste(strsplit(file, '_ANN_input_thigh_2015_feature_set_3.txt')[1], "_predicted_thigh_EE_2015_feature_set_3.csv", sep=""), sep="")
  write.csv(pred_thigh, temp_name)
  print(paste('predicted for thigh 2015_feature_set_3 - ', file))
}

