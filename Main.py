# Link Prediction Package
# Author: Alireza Hajibagheri
# This is a sample file on how to run some of the codes
#============================================================
import sys
sys.path.insert(0, 'SimilarityMetrics')
import numpy as np
from igraph import *
from numpy import genfromtxt
import Create_Train_Set
import Create_Test_Set
import RPM
import Calculate_Unsupervised_AUROC
from sklearn.metrics import auc
import Mix_Sets
import pandas as pd
from sklearn import preprocessing
from Configurations import directory_supervised,from_file,generalization,activeFeatures,feature_importance

# PARAMETERS (DATE, ...)
#===========================================================
RPM_AUROC_Trade = []
directory = directory_supervised
min_max_scaler = preprocessing.MinMaxScaler()
# START
#===========================================================
for ii in range(1,31):
    # Travian files are named based on the day of the 30 days period.
    # The goal here is to read files from day 1 to 30 to create train and
    # test datasets. Message and Trade are names for any arbitrary layers
    # of a network.
    # Modify this part so the code will read your files in order.
    print("ii is : " + str(ii))
    jj = ii + 1
    start = str(ii)
    end = str(jj)
    if ii < 10:
        start = "0" + start
    if jj < 10:
        end = "0" + end
    trainFromDate = "2009-12-" + start
    trainToDate = "2009-12-" + start
    testFromDate = "2009-12-" + end
    testToDate = "2009-12-" + end

    # If you have csv files of networks available, place it in a
    # directory called "Networks" in the same folder as the code is.
    #============================================================
    tradeTrainFile = "trades-train-network-2009-12-" + start + ".txt"

    # Create Graph from the train network file
    # Graph in created for each network (trades or messages) separately
    #============================================================
    print("STEP : Creating Trades Train Graph")
    tradeTrainNetFile = open(directory+tradeTrainFile,'r')
    tradeTrainGraph = Graph.Read_Ncol(tradeTrainNetFile, names=True, weights="if_present", directed=True)
    eTrade = tradeTrainGraph.ecount();vTrade = tradeTrainGraph.vcount()

    # Create Train Set
    #============================================================
    # Randomly select X% of the data (pairs with links) as positive and negative samples
    nPosTrade = int(eTrade*1.0)
    nNegTrade = (vTrade*vTrade) - int(eTrade*1.0)
    nNegTrade = int(nNegTrade*1.0)
    #tradeTrainSet = "trades-train-2009-12-01.txt"
    tradeTrainSet = Create_Train_Set.createTrainSet(tradeTrainGraph,"trades",nPosTrade,nNegTrade,activeFeatures,directory,trainFromDate)
    x_scaled = min_max_scaler.fit_transform(pd.read_csv(directory+tradeTrainSet,sep=" ",header=None))
    tradeTrainDf = pd.DataFrame(x_scaled)
    tradeTrainDf.to_csv(directory+tradeTrainSet, sep=" ", index=False, header=False, float_format='%.6g')

    # If you have csv files of networks available, place it in a
    # directory called "Networks" in the same folder as the code is.
    #============================================================
    tradeTestFile = "trades-test-network-2009-12-" + end + ".txt"

    # Create Graph from the test network file
    #============================================================
    print("STEP : Creating Trades Test Graph")
    tradeTestNetFile = open(directory+tradeTestFile,'r')
    tradeTestGraph = Graph.Read_Ncol(tradeTestNetFile, names=True, weights="if_present", directed=True)
    eTrade = tradeTestGraph.ecount();vTrade = tradeTestGraph.vcount()

    # Create Test Set
    #============================================================
    # Randomly select X% of the data (pairs with links) as positive and negative samples
    nPosTrade = int(eTrade*1.0)
    nNegTrade = (vTrade*vTrade)-int(eTrade*1.0)
    nNegTrade = int(nNegTrade*1.0)
    #tradeTestSet = "trades-test-2009-12-21.txt"
    tradeTestSet = Create_Test_Set.createTestSet(tradeTestGraph,"trades",nPosTrade,nNegTrade,activeFeatures,directory,testFromDate)
    x_scaled = min_max_scaler.fit_transform(pd.read_csv(directory+tradeTestSet,sep=" ",header=None))
    tradeTestDf = pd.DataFrame(x_scaled)
    tradeTestDf.to_csv(directory+tradeTestSet, sep=" ", index=False, header=False, float_format='%.6g')

    # Classification (RPM)
    #============================================================
    numOfFeatures = activeFeatures.count(1)
    tradeAUROC = RPM.classifyData(tradeTrainSet,tradeTestSet,"SVM",numOfFeatures)
    print(" Trade AUROC : " + str(tradeAUROC))
    RPM_AUROC_Trade.append(tradeAUROC)


print("RPM AUROC")
print(RPM_AUROC_Trade)

