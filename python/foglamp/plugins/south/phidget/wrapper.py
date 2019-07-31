from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.LightSensor import *
from Phidget22.Devices.SoundSensor import *
from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.Gyroscope import *
from Phidget22.Devices.Magnetometer import *
from Phidget22.Devices.Encoder import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *


import uuid
import time
from foglamp.plugins.common import utils


class TemperatureSensorWrapper:
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
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
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
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
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
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
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
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

class CurrentInputWrapper:
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
        self.current = CurrentInput()
        self.current.setDeviceSerialNumber(self.hub)
        self.current.setHubPort(self.port)
        self.current.setIsHubPortDevice(False)
        self.current.setChannel(0)
        self.current.openWaitForAttachment(5000)
        try:
            self.current.getCurrent()
        except Exception:
            pass
    def get_reading(self):
        data = {
                'current' : self.current.getCurrent()
        }
        return data
    def close(self):
        self.current.close()
        del(self.current)

class AccelerometerWrapper:
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
        self.accelerometer = Accelerometer()
        self.accelerometer.setDeviceSerialNumber(self.hub)
        self.accelerometer.setHubPort(self.port)
        self.accelerometer.setIsHubPortDevice(False)
        self.accelerometer.setChannel(0)
        self.accelerometer.openWaitForAttachment(5000)
        self.accelerometer.setDataInterval(20)
        for i in range(1,120):
            try:
                self.accelerometer.getAcceleration()
            except Exception:
                time.sleep(1)
                pass
            else:
                break
    def get_reading(self):
        x, y, z = self.accelerometer.getAcceleration()
        data = {
                'x' : x,
                'y' : y,
                'z' : z
        }
        return data
    def close(self):
        self.accelerometer.close()
        del(self.accelerometer)

class GyroscopeWrapper:
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
        self.gyroscope = Gyroscope()
        self.gyroscope.setDeviceSerialNumber(self.hub)
        self.gyroscope.setHubPort(self.port)
        self.gyroscope.setIsHubPortDevice(False)
        self.gyroscope.setChannel(0)
        self.gyroscope.openWaitForAttachment(5000)
        self.gyroscope.setDataInterval(20)
        for i in range(1,120):
            try:
                self.gyroscope.getAngularRate()
            except Exception:
                time.sleep(1)
                pass
            else:
                break
    def get_reading(self):
        x, y, z = self.gyroscope.getAngularRate()
        data = {
                'x' : x,
                'y' : y,
                'z' : z
        }
        return data
    def close(self):
        self.gyroscope.close()
        del(self.gyroscope)

class MagnetometerWrapper:
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
        self.magnetometer = Magnetometer()
        self.magnetometer.setDeviceSerialNumber(self.hub)
        self.magnetometer.setHubPort(self.port)
        self.magnetometer.setIsHubPortDevice(False)
        self.magnetometer.setChannel(0)
        self.magnetometer.openWaitForAttachment(5000)
        self.magnetometer.setDataInterval(20)
        for i in range(1,120):
            try:
                self.magnetometer.getMagneticField()
            except Exception:
                time.sleep(1)
                pass
            else:
                break
    def get_reading(self):
        x, y, z = self.magnetometer.getMagneticField()
        data = {
                'x' : x,
                'y' : y,
                'z' : z
        }
        return data
    def close(self):
        self.magnetometer.close()
        del(self.magnetometer)

class RotaryEncoderWrapper:
    def __init__(self, hub, port, assetName, poll):
        self.hub = hub
        self.port = port
        self.assetName = assetName
        self.poll = poll
        self.count = 0
        self.prevPosition = None
        self.prevTime = None
        self.encoder = Encoder()
        self.encoder.setDeviceSerialNumber(self.hub)
        self.encoder.setHubPort(self.port)
        self.encoder.setIsHubPortDevice(False)
        self.encoder.setChannel(0)
        self.encoder.openWaitForAttachment(5000)
        self.encoder.setDataInterval(20)
        for i in range(1,120):
            try:
                self.encoder.getPosition()
            except Exception:
                time.sleep(1)
                pass
            else:
                break
    def get_reading(self):
        if self.prevPosition is None or self.prevTime is None:
            self.prevPosition = self.encoder.getPosition()
            self.prevTime = time.time()
            return None
        currentPosition = self.encoder.getPosition()
        currentTime = time.time()
        secondsDelta = currentTime - self.prevTime
        rotationsDelta = (currentPosition  - self.prevPosition)/1200.00
        rpm = (rotationsDelta/secondsDelta)*60
        data = {
                'rotationsdelta' : rotationsDelta,
                'secondsdelta' : secondsDelta,
                'rpm' : rpm
        }
        self.prevPosition = currentPosition
        self.prevTime = currentTime
        return data
    def close(self):
        self.encoder.close()
        del(self.encoder)
