import dbOperations
import cnfOperations
import pandas as pd
import numpy as np
import math
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.inspection import *
from sklearn.ensemble import IsolationForest
import pickle
from datetime import datetime

class ModelCreator():
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
    def createForecastModels(self):
        for index, row in self.dfSensors.iterrows():
            print(row)
            # prepare model dataset
            index = row["deviceId"]
            PrevSensorEUI = str(row["prevDeviceId"])
            PrevSensorsEUI = PrevSensorEUI.split(',')
            #print(row["prevDeviceId"])
            #print(PrevSensorEUI)
            NextSensorEUI = str(row["nextDeviceId"])
            NextSensorsEUI = NextSensorEUI.split(',')
            #print(row["nextDeviceId"])
            #print(NextSensorsEUI)

            dfYSensor = dbOperations.DbOperation.readFromAnalyticsCollection("Analytics", "devicetempshist", {"deviceId":index}, 1)
            dfYSensor = dfYSensor.sort_values(by=['datetime'])
            dfValues = dfYSensor[["temp", "datetime"]]
            dfValues.columns = ["target", "datetime"]
            print(dfValues["datetime"].head())
            dfValues["hour"] = dfValues.apply(lambda x: float(str(x["datetime"])[11:13]), axis=1)
            dfValues["haftaici"] = dfValues.apply(lambda x: self.getWorkingDay(x["datetime"]), axis=1)     

            print(dfValues.head())
            
            for sensorEUI in PrevSensorsEUI:
                if (sensorEUI != "nan"):
                    indexS = sensorEUI
                    dfXSensor = dbOperations.DbOperation.readFromAnalyticsCollection("Analytics", "devicetempshist", {"deviceId":indexS}, 1)
                    dfXValues = dfXSensor[["temp", "datetime"]]
                    dfXValues.columns = [str(sensorEUI), "datetime"]
                    dfValues = dfValues.merge(dfXValues, on='datetime', how='left')
                    #dfValues = pd.concat([dfValues, dfXValues], axis=1, sort=False)
                    
            for sensorEUI in NextSensorsEUI:
                if (sensorEUI != "nan"):
                    indexS = sensorEUI
                    dfXSensor = dbOperations.DbOperation.readFromAnalyticsCollection("Analytics", "devicetempshist", {"deviceId":indexS}, 1)
                    dfXValues = dfXSensor[["temp", "datetime"]]
                    dfXValues.columns = [str(sensorEUI), "datetime"]
                    dfValues = dfValues.merge(dfXValues, on='datetime', how='left')
                    #dfValues = pd.concat([dfValues, dfXValues], axis=1, sort=False)

            dfValues = dfValues.drop("datetime", axis=1)
            dfValues.drop_duplicates(inplace= True)
            dfValues = dfValues[dfValues.notna()]
            columns = dfValues.columns
            for column in columns:
                dfValues = dfValues[dfValues[column]>0]

            dfValues["anomaly"] = 0

            print(dfValues.head(5))

            x, y = dfValues.shape

            outliers_fraction = 0.01
            for i in range(3,y-1):
                dfIso = dfValues[["target"]].copy()
                dfIso[columns[i]] = dfValues[[columns[i]]].copy()
                X = np.array(dfIso)
                model = IsolationForest(contamination=outliers_fraction, random_state=42)
                iso_pred = model.fit(X).predict(X)
                df_iso_pred = pd.DataFrame(iso_pred, columns=["iso"])
                print(df_iso_pred.head())
                dfValues["anomaly"] = dfValues["anomaly"] + df_iso_pred["iso"]

            filt = y-4
            print(dfValues.head())

            dfValues = dfValues[dfValues["anomaly"]==filt]
            k, l = dfValues.shape

            if(k==0):
                continue

            print(dfValues.head())
            dfValues.drop(['anomaly'], axis=1, inplace=True)
            if(x>5):
                dfY = dfValues[["target"]]
                dfX = dfValues.drop("target", axis=1)

                train_size = int(len(dfValues)* self.train_test_split_size)
                dfXTrain = dfX[0:train_size]
                dfXTest = dfX[train_size:len(dfValues)]
                dfYTrain = dfY[0:train_size]
                dfYTest = dfY[train_size:len(dfValues)]

                modelMLP = MLPRegressor(random_state=1, max_iter=500)
                modelMLP.fit(dfXTrain, dfYTrain)
                y_predTest = modelMLP.predict(dfXTest)
                y_predTrain = modelMLP.predict(dfXTrain)

                print(dfYTest["target"].to_numpy(dtype='float'))
                print(y_predTest)

                #acc = modelMLP.score(dfYTest["target"].to_numpy().reshape(-1,1), y_predTest.reshape(-1,1))
                #acc = modelMLP.score(dfYTest, y_predTest)


                rmseTest = np.sqrt(mean_squared_error(dfYTest, y_predTest))
                rmseTrain = np.sqrt(mean_squared_error(dfYTrain, y_predTrain))

                print("rmse_test: ", rmseTest)
                print("rmse_train: ", rmseTrain)
                #print("accuracy: ", acc)

                
                # save the model to disk
                if((rmseTest < 2) and (rmseTrain < 2)):
                    filename = "model_" + str(index) + ".sav"
                    pickle.dump(modelMLP, open(filename, 'wb'))
                    print("Model saved")
                    
                
            """
            # Anomally detection model for the system begins

            # Anomally detection model for the system ends

            # Anomally detection model for the sensor begins

            # Anomally detection model for the sensor ends
            """