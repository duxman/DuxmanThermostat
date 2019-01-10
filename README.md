# DuxmanThermostat
DuxmanThermostat

### **Install instructions**

**Packages** 

sudo apt-get update

sudo apt-get install build-essential python-dev python-openssl git

sudo apt install apt-transport-https

curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get install influxdb

sudo apt-get install python-pip python-influxdb

curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -

echo "deb https://dl.bintray.com/fg2it/deb-rpi-1b stretch main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

sudo apt-get update

sudo apt-get install grafana


**Download APIs**

git clone https://github.com/adafruit/Adafruit_Python_DHT.git 
cd Adafruit_Python_DHT
sudo python setup.py install
