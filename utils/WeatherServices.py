import os
from time import gmtime, strftime


if os.name == 'poxis':
    import Adafruit_DHT
else:
    from emulator.emulators import emulator_Adafruit_DHT
    Adafruit_DHT = emulator_Adafruit_DHT()
    EMULATE = True

class DHT22(object):
    SensorType = None
    SensorGpio = 17
    TableData = "None"
    Location = "None"
    Logger = None

    def __init__(self,sensortype, sensorgpio, tabledata,location,logger):
        self.SensorGpio = sensorgpio
        self.SensorType = sensortype
        self.TableData = tabledata
        self.Location = location
        self.Logger = logger

    def GetDHTLocalSensor(self):

        humidity, temperature = Adafruit_DHT.read_retry( sensortype=self.SensorType, sensorpin=self.SensorGpio)

        iso = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data = self.GenerateJsonData(timeset=iso, humidity=humidity, temperature=temperature)

        self.Logger.info("data time : " + iso + " hum: " + str( humidity) + " temp: " + str(temperature) )

        return data

    def GenerateJsonData(self, timeset, humidity, temperature):
        data = [{"measurement": self.TableData,"tags": {"location": self.Location,},"time":timeset,"fields": {"temperature": temperature,"humidity": humidity}}]
        return data