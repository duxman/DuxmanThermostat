import os
import Adafruit_DHT

# if os.name == 'poxis':
#    import Adafruit_DHT
# else:
#    from emulator.emulators import emulator_Adafruit_DHT
#    Adafruit_DHT = emulator_Adafruit_DHT()
#    EMULATE = True

from  queue import Queue
from utils.Config import ConfigLoader
from utils.StopableThread import StopableConsumerThread, StopableProduceThread
from utils.WeatherServices import DHT22, OWM
from utils.logger import clienteLog
#from influx import InfluxDB
from influxdb import InfluxDBClient



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
        self.Logger.info(data)
        self.DBClient.write_points(data)

    def CreateConsumerThreat(self):
        self.ThermostatConsumerThreat =  StopableConsumerThread( queue = self.WorkingQueue,target = self.WriteInfluxData, sleep = 1, name = "ConsumerThermostatThreat", logger=self.Logger)
        self.ThermostatConsumerThreat.start()

    def CreateProducerThreat(self, name, target,sleeptime):
        t =  StopableProduceThread(queue = self.WorkingQueue,target = target, sleep = sleeptime, name = name, logger=self.Logger)
        t.start()
        self.WorkingQueue.join()
        self.ThermostatProducerThreats.append(t)

    def ConfigLoader(self):
        self.Configuration = ConfigLoader();

    def CreateWeatherServices(self):
        self.Dht22Service = DHT22(Adafruit_DHT.DHT22,17, self.Configuration.TableData,"SENSOR 1", self.Logger)
        self.OWMService = OWM(self.Configuration.TableData,"Exterior",self.Logger)

    def __init__(self):
        cliente = clienteLog()
        self.Logger = cliente.InicializaLog()

        self.ConfigLoader()

        self.WorkingQueue = Queue()
        self.DBClient =  InfluxDBClient('localhost', 8086,"logger","logger","sensor_data")
        self.Configuration.TableData = "DuxmanThermostat"
        self.Configuration.Location = "Emulation Place"
        self.Configuration.SleepTime = 60
        self.CreateConsumerThreat()

        self.CreateWeatherServices()

        self.CreateProducerThreat(name="DHT22LocalSensorThreatProducer", target=self.Dht22Service.GetData,sleeptime=10 )
        self.CreateProducerThreat(name="OWMSensorThreatProducer", target=self.OWMService.GetData,sleeptime=self.Configuration.SleepTime)

if __name__ == "__main__":
    mainprogram = DuxmanThermostat()
    mainprogram.Logger.info("--------------------<<  END  >>--------------------")
