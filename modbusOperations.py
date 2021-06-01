from pyModbusTCP.client import ModbusClient
import cnfOperations as cnf
import sys
import math
import numpy as np

class ModbusOperation():
    @staticmethod
    def readFromModBus(sensorNo, lineNo, sensorType):
        try:
            myHost = cnf.cnfOperation.readModBusHost()
            sensorTypeNo = 0
            if(sensorType == "L1"):
                sensorTypeNo = 1
            elif(sensorType == "L2"):
                sensorTypeNo = 2
            elif(sensorType == "L3"):
                sensorTypeNo = 3
            elif(sensorType == "OUT"):
                sensorTypeNo = 7

            groupNo = math.floor(((lineNo -1) / 256)) + 1 
            portNo = 10000 + (sensorTypeNo -1) * 10 + groupNo - 1
            regNo = (((lineNo - 1) * 128 + (sensorNo - 1)) * 2) % 65536

            '''
            print("groupNo:" , groupNo)
            print("portNo:" , portNo)
            print(((lineNo - 1) * 128 + (sensorNo - 1)) * 2)
            print("regNo:" , regNo)
            print("host:", myHost)
            '''
            
            myClient = ModbusClient(host = myHost, port = portNo, unit_id = 1, auto_open = True)
            myClient.open()
            regs = myClient.read_holding_registers(regNo, 2)

            #print(regs)
            regs[0], regs[1] = regs[1], regs[0]
            data_bytes = np.array(regs, dtype=np.uint16)
            result = data_bytes.view(dtype=np.float32)
            myClient.close()
            #print(result[0])
            return result[0]
        
        except Exception as e:
            print(e.__class__," occured.")
            print(e.values)
            print("Could not read from modbus")
            sys.exit(-1)

    @staticmethod
    def readSensorTempDiff(lineNo, sensorNo):
        print("Line: ",lineNo)
        print("Sensor: ",sensorNo)
        temp1 = ModbusOperation.readFromModBus(sensorNo, lineNo, "L1")
        temp2 = ModbusOperation.readFromModBus(sensorNo, lineNo, "L2")
        temp3 = ModbusOperation.readFromModBus(sensorNo, lineNo, "L3")
        temp4 = ModbusOperation.readFromModBus(sensorNo, lineNo, "OUT")

        maks = max(temp1,temp2,temp3)
        diff = maks - temp4
        return (maks, diff)



        
