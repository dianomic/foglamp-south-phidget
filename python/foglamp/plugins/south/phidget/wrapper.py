from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.LightSensor import *
from Phidget22.Devices.SoundSensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *


import uuid
from foglamp.plugins.common import utils


class TemperatureSensorWrapper:
    def __init__(self, hub, port, assetName):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.temp = TemperatureSensor()
        self.temp.setDeviceSerialNumber(self.hub)
        self.temp.setHubPort(self.port)
        self.temp.setIsHubPortDevice(False)
        self.temp.setChannel(0)
        self.temp.openWaitForAttachment(5000)
        try:
            self.temp.getTemperature()
        except Exception:
            pass
    def get_reading(self):
        data = {
                'temperature' : self.temp.getTemperature()
        }
        return data
    def close(self):
        self.temp.close()
        del(self.temp)

class HumiditySensorWrapper:
    def __init__(self, hub, port, assetName):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.hum = HumiditySensor()
        self.hum.setDeviceSerialNumber(self.hub)
        self.hum.setHubPort(self.port)
        self.hum.setIsHubPortDevice(False)
        self.hum.setChannel(0)
        self.hum.openWaitForAttachment(5000)
        try:
            self.hum.getHumidity()
        except Exception:
            pass
    def get_reading(self):
        data = {
                'humidity' : self.hum.getHumidity()
        }
        return data
    def close(self):
        self.hum.close()
        del(self.hum)

class LightSensorWrapper:
    def __init__(self, hub, port, assetName):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.light = LightSensor()
        self.light.setDeviceSerialNumber(self.hub)
        self.light.setHubPort(self.port)
        self.light.setIsHubPortDevice(False)
        self.light.setChannel(0)
        self.light.openWaitForAttachment(5000)
        try:
            self.light.getIlluminance()
        except Exception:
            pass
    def get_reading(self):
        data = {
                'lumens' : self.light.getIlluminance()
        }
        return data
    def close(self):
        self.light.close()
        del(self.light)

class SoundSensorWrapper:
    def __init__(self, hub, port, assetName):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.sound = SoundSensor()
        self.sound.setDeviceSerialNumber(self.hub)
        self.sound.setHubPort(self.port)
        self.sound.setIsHubPortDevice(False)
        self.sound.setChannel(0)
        self.sound.openWaitForAttachment(5000)
        try:
            self.sound.getdB()
        except Exception:
            pass
    def get_reading(self):
        data = {
                'sound' : self.sound.getdB()
        }
        return data
    def close(self):
        self.sound.close()
        del(self.sound)
