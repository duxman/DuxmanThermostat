import os
if os.name == 'poxis':
    import Adafruit_DHT
else:
    from emulator.emulators import emulator_Adafruit_DHT
    Adafruit_DHT = emulator_Adafruit_DHT()
    EMULATE = True

from  queue import Queue
from utils.Config import ConfigLoader
from utils.StopableThread import StopableConsumerThread, StopableProduceThread
from utils.WeatherServices import DHT22, OWM
from utils.logger import clienteLog
from influx import InfluxDB



class DuxmanThermostat(object):
    Logger = None
    WorkingQueue = None
    DBClient = None
    Configuration = None
    ThermostatConsumerThreat = None
    ThermostatProducerThreats = []
    Dht22Service = None
    OWMService = None

    def WriteInfluxData(self,data):
        self.DBClient.write_points(data)

    def CreateConsumerThreat(self):
        self.ThermostatConsumerThreat =  StopableConsumerThread( queue = self.WorkingQueue,target = self.WriteInfluxData, sleep = self.Configuration.SleepTime, name = "ConsumerThermostatThreat", logger=self.Logger)
        self.ThermostatConsumerThreat.setDaemon( True )
        self.ThermostatConsumerThreat.start()

    def CreateProducerThreat(self, name, target):
        t =  StopableProduceThread(queue = self.WorkingQueue,target = target, sleep = self.Configuration.SleepTime, name = name, logger=self.Logger)
        t.start()
        self.WorkingQueue.join()
        self.ThermostatProducerThreats.append(t)

    def ConfigLoader(self):
        self.Configuration = ConfigLoader();

    def CreateWeatherServices(self):
        self.Dht22Service = DHT22("NONE",17, self.Configuration.TableData,self.Configuration.Location, self.Logger)
        self.OWMService = OWM(self.Configuration.TableData,self.Configuration.Location,self.Logger)

    def __init__(self):
        cliente = clienteLog()
        self.Logger = cliente.InicializaLog()

        self.ConfigLoader()

        self.WorkingQueue = Queue()

        self.DBClient =  InfluxDB(self.Configuration.DBUrl)

        if ( EMULATE == True ):
            self.Configuration.SleepTime = 60
            self.Configuration.TableData = "Emulation"
            self.Configuration.Location = "Emulation Place"
        else :
            self.CreateConsumerThreat()

        self.CreateWeatherServices()

        self.CreateProducerThreat(name="DHT22LocalSensorThreatProducer", target=self.Dht22Service.GetData )
        self.CreateProducerThreat(name="OWMSensorThreatProducer", target=self.OWMService.GetData)

if __name__ == "__main__":
    mainprogram = DuxmanThermostat()
    mainprogram.Logger.info("--------------------<<  END  >>--------------------")