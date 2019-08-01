
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

# Configuration
The foglamp-south-phidget configuration has two configuration entries:
Asset Name Prefix - a string to prefix the asset name for all assets of an instance of this plugin.
Phidget Map - a JSON object specifying the VINT hubs and corresponding sensors to ingest data from.

* Example: Single hub, single sensor
In the following example, we are connecting a single temperature sensor connected to a single VINT hub on port 0.
The hubSN is the VINT hub serial number to connect to. 
The sensorType is TemperatureSensor (look at the "Supported Sensor Modules" table for currently support sensorType entries. 
The assetName we chose to use is "temperature01", but it is configurable to what the user chooses.
The port is the port of the VINT hub the sensor is connected to.
The poll is 1, which specifies that the temeprature sensor should be polled every time the plugin is polled. So if a plugin is polled once a second, the temperature sensor is also polled once a second.

```
{
  "values": [
    {
      "hubSN": 538395,
      "sensorType": "TemperatureSensor",
      "poll": 1,
      "assetName": "temperature01",
      "port": 0
    }
  ]
}
```


* Example: Single hub, two sensors
In the following example, in a single VINT hub, we are connecting a temperature sensor on port 0 and a sound sensor on port 1.
The sensorType is SoundSensor. 
The assetName we chose to use is "soundlevel", but it is configurable to what the user chooses.
The poll is 10, which specifies that the sound sensor should be polled every tenth time the plugin is polled. So if the plugin is polled every second, the sound sensor will be polled every tenth second. The temperature sensor will still be polled every second.

```
{
  "values": [
    {
      "hubSN": 538395,
      "sensorType": "TemperatureSensor",
      "poll": 1,
      "assetName": "temperature01",
      "port": 0
    },
    {
      "hubSN": 538395,
      "sensorType": "SoundSensor",
      "poll": 10,
      "assetName": "soundlevel",
      "port": 2
    }
  ]
}
```

* Example: Two hubs, three sensors
In the following example, one VINT hub is connecting a temperature sensor on port 0 and a sound sensor on port 1 while another CINT hub is connected to another temperture sensor.
The hubSN for the new entry is different that the first two, as it is connected to a separate VINT hub.
The sensorType is Temperature Sensor, but we specify a different assetName "temperature02", to differentiate from the other temperature sensor "temperature03".
```
{
  "values": [
    {
      "hubSN": 538395,
      "sensorType": "TemperatureSensor",
      "poll": 1,
      "assetName": "temperature01",
      "port": 0
    },
    {
      "hubSN": 538395,
      "sensorType": "SoundSensor",
      "poll": 10,
      "assetName": "soundlevel",
      "port": 2
    }
    {
      "hubSN": 561266,
      "sensorType": "TemperatureSensor",
      "poll": 1,
      "assetName": "temperature02",
      "port": 0
    },
  ]
}
```

* Example: all sensors we have tested
The following example shows configuration for all sensors we have connected and tested so far.
```
{
  "values": [
    {
      "hubSN": 561266,
      "sensorType": "TemperatureSensor",
      "poll": 10,
      "assetName": "temperature1",
      "port": 0
    },
    {
      "hubSN": 561266,
      "sensorType": "HumiditySensor",
      "poll": 10,
      "assetName": "humidity1",
      "port": 0
    },
    {
      "hubSN": 561266,
      "sensorType": "SoundSensor",
      "poll": 10,
      "assetName": "sound",
      "port": 1
    },
    {
      "hubSN": 561266,
      "sensorType": "LightSensor",
      "poll": 10,
      "assetName": "light",
      "port": 2
    },
    {
      "hubSN": 561266,
      "sensorType": "CurrentInput",
      "poll": 1,
      "assetName": "current",
      "port": 3
    },
    {
      "hubSN": 561266,
      "sensorType": "Accelerometer",
      "poll": 1,
      "assetName": "accelerometer",
      "port": 4
    },
    {
      "hubSN": 561266,
      "sensorType": "Gyroscope",
      "poll": 1,
      "assetName": "gyroscope",
      "port": 4
    },
    {
      "hubSN": 561266,
      "sensorType": "Magnetometer",
      "poll": 1,
      "assetName": "magnetometer",
      "port": 4
    },
    {
      "sensorType": "Encoder",
      "hubSN": 561266,
      "assetName": "rotary",
      "pulsesPerRevolution": 1200,
      "poll": 10,
      "port": 5
    }
  ]
}
```
