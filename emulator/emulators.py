import random


class emulator_Adafruit_DHT(object):
    DHT22 = "NONE"
    def read_retry(self,sensortype="Emulation", sensorpin=17):
        h = random.randint(0,100)
        t = random.randint(-10,60)
        return h,t