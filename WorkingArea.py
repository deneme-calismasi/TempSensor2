import dbOperations
import encoder
import pandas as pd
from datetime import datetime
import time
import modelCreator as mc
import modbusOperations
import cnfOperations as cnf

result = cnf.cnfOperation.readLineInfo()
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data = list()

#print(len(result))
for prop in result:
    line = int(prop)
    print("Line: ", prop)
    val = result[prop]
    vals = val.split(',')
    startSen = int(vals[1])
    endSen = int(vals[2])
    print("Başlangıç: ", vals[0])
    print("Min Sensor No: ", startSen)
    print("Max Sensor No: ", endSen)

    for i in range(startSen, endSen+1):
        
        row = list()
        maks = modbusOperations.ModbusOperation.readSensorTempDiff(line,i)[0]
        diff = modbusOperations.ModbusOperation.readSensorTempDiff(line,i)[1]
        row.append(line)
        row.append(i)
        row.append(time)
        row.append(maks)
        row.append(diff)
        print(row)
        data.append(row)

df = pd.DataFrame(data)
df.columns = ["Line", "Sensor", "Time", "Temp", "TempDiff"]
print(df.head())
insertedIds = dbOperations.DbOperation.writeToAnalyticsCollection("Analytics","devicetempshist",df)

'''
temp1 = modbusOperations.ModbusOperation.readFromModBus(1,1,"L1")
print(temp1)

temp2 = modbusOperations.ModbusOperation.readFromModBus(1,1,"L2")
print(temp2)

temp3 = modbusOperations.ModbusOperation.readFromModBus(1,1,"L3")
print(temp3)

temp4 = modbusOperations.ModbusOperation.readFromModBus(1,1,"OUT")
print(temp4)
'''

#print(modbusOperations.ModbusOperation.readSensorTempDiff(1,3))


"""
dfSensors = dbOperations.DbOperation.readFromLogCollection("DeviceLog", "devicetemps")
print(dfSensors.head())
print(dfSensors["lastTempLog"].iloc[0])
tempStr = dfSensors["lastTempLog"].iloc[0]
print(tempStr["L1"])
print(tempStr["L2"])
print(tempStr["L3"])
print(tempStr["OUT"])


import historyCreator as hc

hst = hc.HistoryCreator()
hst.createHistory()
"""

"""
mongodb useful codes:
db.devicetempshist.deleteMany({})
db.devicetempshist.count()
db.getCollection('devicetempshist').find({})
db.getCollection('devicetempshist').find({deviceId:'L1_D09'}).sort({datetime:1})
db.getCollection('devicetemps').find({"deviceId":/L1/})
{"deviceId":/L0001_D002/}

"""


"""

dfSensors = pd.read_csv("deviceMap.csv", sep=";")
dbOperations.DbOperation.writeToAnalyticsCollection("Analytics","deviceinfo",dfSensors)

"""
'''
mdc = mc.ModelCreator()
mdc.createForecastModels()
'''

'''
x= "2021-02-02"
year = int(x[0:4])
month = int(x[5:7])
day = int(x[8:10])

x = datetime(year, month, day)

dayW = int(x.strftime("%w"))
if((dayW == 0) or (dayW == 6)):
    print("haftasonu")
else:
    print("haftaici")

'''


