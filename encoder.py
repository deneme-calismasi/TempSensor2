import base64
import struct


class Encoder():
    @staticmethod
    def getValues(hexValue):
        sensors = base64.b64decode(hexValue).hex()
        sensor1 = struct.unpack('!f', bytes.fromhex(sensors[0:8]))[0]
        sensor2 = struct.unpack('!f', bytes.fromhex(sensors[8:16]))[0]
        sensor3 = struct.unpack('!f', bytes.fromhex(sensors[16:24]))[0]
        sensor4 = struct.unpack('!f', bytes.fromhex(sensors[24:32]))[0]
        sensor5 = struct.unpack('!f', bytes.fromhex(sensors[32:40]))[0]

        return (sensor1, sensor2, sensor3, sensor4, sensor5)
