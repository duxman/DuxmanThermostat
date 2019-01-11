import os
from time import gmtime, strftime

from requests import get
from datetime import datetime, timedelta
from json import loads
from pprint import pprint
KEY = 'f16f71ea347b7edc2b755bc39228f56b'
CITY_ID = 3104323
# {
#     "id": 3104323,
#     "name": "Provincia de Zaragoza",
#     "country": "ES",
#     "coord": {
#         "lon": -1,
#         "lat": 41.583328
#     }

if os.name == 'poxis':
    import Adafruit_DHT
else:
    from emulator.emulators import emulator_Adafruit_DHT
    Adafruit_DHT = emulator_Adafruit_DHT()
    EMULATE = True

class SensorData(object):
    TableData = "None"
    Location = "None"
    Logger = None

    def __init__(self,tabledata,location,logger):
        self.TableData = tabledata
        self.Location = location
        self.Logger = logger


    def GenerateJsonData(self, timeset, humidity, temperature):
        data = [{"measurement": self.TableData,"tags": {"location": self.Location,},"time":timeset,"fields": {"temperature": temperature,"humidity": humidity}}]
        return data

class DHT22(SensorData):
    SensorType = None
    SensorGpio = 17


    def __init__(self,sensortype, sensorgpio, tabledata,location,logger):

        SensorData.__init__(self, tabledata, location,logger)

        self.SensorGpio = sensorgpio
        self.SensorType = sensortype



    def GetData(self):

        humidity, temperature = Adafruit_DHT.read_retry( sensortype=self.SensorType, sensorpin=self.SensorGpio)

        iso = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data = self.GenerateJsonData(timeset=iso, humidity=humidity, temperature=temperature)

        self.Logger.info("Data name : " + self.__class__.__name__ + " time : " + iso + " hum: " + str( humidity) + " temp: " + str(temperature) )

        return data

class OWM(SensorData):

    def __init__(self, tabledata, location,logger):
        SensorData.__init__(self, tabledata, location,logger)


    def get_weather_data(self, city_id = CITY_ID, getforecast = False ):
        # for forecast
        datatype = "weather"
        if( getforecast == True ):
            datatype = "forecast"

        weather_data = get('http://api.openweathermap.org/data/2.5/{}?id={}&APPID={}&units=metric'.format(datatype,city_id, KEY))

        data = weather_data.json()
        # get only temperature and humidity
        humidity = data["main"]["humidity"]
        temperature = data["main"]["temp"]

        return humidity,temperature

    def GetData(self):

        humidity, temperature = self.get_weather_data( CITY_ID)

        iso = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data = self.GenerateJsonData(timeset=iso, humidity=humidity, temperature=temperature)

        self.Logger.info("Data name : " + self.__class__.__name__ + " time : " + iso + " hum: " + str(humidity) + " temp: " + str(temperature))

        return data
