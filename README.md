
# Prerequisites
The foglamp-south-phidget plugin requires libusb-1.0.0-dev, libphidget22, and the Phidget Python module. 

The packages can be installed with given [extras_install.sh](extras_install.sh) or manual with below steps:


# Install 
* [System](https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads)
``` 
# install libusb
apt-get install libusb-1.0.0-dev

# install libphidget22
rm -rf /tmp/foglamp-phidget-install
mkdir /tmp/foglamp-phidget-install
cd /tmp/foglamp-phidget-install
wget https://www.phidgets.com/downloads/phidget22/libraries/linux/libphidget22.tar.gz
tar -xzvf libphidget22.tar.gz
cd libphidget22-*
./configure --prefix=/ && make && make install
fn=`find -name *libphidget22.rule*`

# add udev rule file to allow access to the Phidget when running from non-root user
mv `find -name *libphidget22.rule*` /etc/udev/rules.d/.
cd
rm -rf /tmp/foglamp-phidget-install

``` 

* [Python](https://www.phidgets.com/docs/Language_-_Python) 
```
# install Phidget python module
pip3 install -r python/requirements-phidget.txt

```


# Supported Sensor Modules
| sensorType          | Phidget Python Class | Tested Phidget Sensors |
| ------------------- | -------------------- | -------------- |
| HumiditySensor      | HumiditySensor       | [HUM1000_0](https://www.phidgets.com/?tier=3&catid=14&pcid=12&prodid=644) |
| TemperatureSensor   | TemperatureSensor    | [HUM1000_0](https://www.phidgets.com/?tier=3&catid=14&pcid=12&prodid=644) |
| LightSensor         | LightSensor          | [LUX1000_0](https://www.phidgets.com/?tier=3&catid=8&pcid=6&prodid=707)   |
| SoundSensor         | SoundSensor          | [SND1000_0](https://www.phidgets.com/?tier=3&catid=8&pcid=6&prodid=972)   |
| CurrentInput        | CurrentInput         | [VCP1100_0](https://www.phidgets.com/?tier=3&catid=16&pcid=14&prodid=983) |
| Accelerometer       | Accelerometer        | [MOT1101_0](https://www.phidgets.com/?tier=3&catid=10&pcid=8&prodid=975) |
| Gyroscope           | Gyroscope            | [MOT1101_0](https://www.phidgets.com/?tier=3&catid=10&pcid=8&prodid=975) |
| Magnetometer        | Magnetometer         | [MOT1101_0](https://www.phidgets.com/?tier=3&catid=10&pcid=8&prodid=975) |
| Encoder             | Encoder              | [ENC1000_0](https://www.phidgets.com/?tier=3&catid=4&pcid=2&prodid=959) + [3531_0](https://www.phidgets.com/?tier=3&catid=103&pcid=83&prodid=404) |



