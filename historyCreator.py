import dbOperations
import pandas as pd
from datetime import datetime


class HistoryCreator():
    def __init__(self):
        self.dfSensors = dbOperations.DbOperation.readFromLogCollection("DeviceLog", "devicetemps")

    def createHistory(self):
        sensorList = list()
        deltaTempList = list()

        for index, row in self.dfSensors.iterrows():
            sensor = row["deviceId"]
            print(sensor)
            try:
                L1 = float(row["lastTempLog"]["L1"])
            except:
                L1 = -300.0
                print("Hatalı Veri")
                # continue
            print(L1)
            try:
                L2 = float(row["lastTempLog"]["L2"])
            except:
                L2 = -300.0
                print("Hatalı Veri")
                # continue
            print(L2)
            try:
                L3 = float(row["lastTempLog"]["L3"])
            except:
                L3 = -300.0
                print("Hatalı Veri")
                # continue
            print(L3)
            try:
                OUT = float(row["lastTempLog"]["OUT"])
            except:
                OUT = -300.0
                print("Hatalı Veri")
                # continue
            print(OUT)

            sensorList.append(sensor)
            deltaTempList.append(max((L1 - OUT), (L2 - OUT), (L3 - OUT)))

        dfWrite = pd.DataFrame(zip(sensorList, deltaTempList), columns=['deviceId', 'temp'])
        dfWrite["datetime"] = datetime.now()

        print(dfWrite.head())
        dbOperations.DbOperation.writeToAnalyticsCollection("Analytics", "devicetempshist", dfWrite)
        print("Data inserted into Analytics historical table")
