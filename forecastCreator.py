import dbOperations
import cnfOperations
import pandas as pd
import numpy as np
import math
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.inspection import *
from sklearn.ensemble import IsolationForest
import pickle

class ForecastCreator():
    def __init__(self):
        self.dfSensors = dbOperations.DbOperation.readFromAnalyticsCollection("Analytics","deviceinfo")
        self.train_test_split_size = float(cnfOperations.cnfOperation.readTrainTestSplitSize())
    def getWorkingDay(self,x):
        year = int(str(x)[0:4])
        month = int(str(x)[5:7])
        day = int(str(x)[8:10])
        x = datetime(year, month, day)
        dayW = int(x.strftime("%w"))
        if((dayW == 0) or (dayW == 6)):
            return 0
        else:
            return 1
    def createForecast(self):
        for index, row in self.dfSensors.iterrows():
            print(row)
            # prepare model dataset
            index = row["deviceId"]
            PrevSensorEUI = str(row["prevDeviceId"])
            PrevSensorsEUI = PrevSensorEUI.split(',')
            #print(row["prevDeviceId"])
            #print(PrevSensorsEUI)
            NextSensorEUI = str(row["nextDeviceId"])
            NextSensorsEUI = NextSensorEUI.split(',')
            #print(row["nextDeviceId"])
            #print(NextSensorsEUI)

            
            dfYSensor = dbOperations.DbOperation.readLastFromAnalyticsCollection("Analytics", "devicetempshist", {"deviceId":index}, 1)
            dfValues = dfYSensor[["temp", "datetime"]]
            actTemp = float(dfValues.iloc[0,0])
            actDate = float(dfValues.iloc[0,1])

            #print(dfValues.head())
            data = list()
            prediction = 0.0
            
            for sensorEUI in PrevSensorsEUI:
                if (sensorEUI != "nan"):
                    indexS = sensorEUI
                    dfXSensor = dbOperations.DbOperation.readLastFromAnalyticsCollection("Analytics", "devicetempshist", {"deviceId":indexS}, 1)
                    dfXValues = dfXSensor[["temp", "datetime"]]
                    prevTemp = float(dfXValues.iloc[0,0])
                    prevDate = float(dfXValues.iloc[0,1])
                    if(actDate == prevDate):
                        data.append(prevTemp)
                    else:
                        data.append(-300.0)

                    #dfValues = pd.concat([dfValues, dfXValues], axis=1, sort=False)
                    
            for sensorEUI in NextSensorsEUI:
                if (sensorEUI != "nan"):
                    indexS = sensorEUI
                    dfXSensor = dbOperations.DbOperation.readLastFromAnalyticsCollection("Analytics", "devicetempshist", {"deviceId":indexS}, 1)
                    dfXValues = dfXSensor[["temp", "datetime"]]
                    nextTemp = float(dfXValues.iloc[0,0])
                    nextDate = float(dfXValues.iloc[0,1])
                    if(actDate == nextDate):
                        data.append(nextTemp)
                    else:
                        data.append(-300.0)
                    #dfValues = pd.concat([dfValues, dfXValues], axis=1, sort=False)

            dfData = pd.Dataframe(data)

            # load the model from disk
            filename = 'model_' + index + '.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            prediction = loaded_model.predict(dfData)
            print("sersor:",index," , actual:", actTemp, " , prediction:" , prediction)
            