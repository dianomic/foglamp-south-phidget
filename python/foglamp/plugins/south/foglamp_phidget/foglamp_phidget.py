# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END

""" Module for Phidget poll mode plugin

    The following is intended as the south service plugin of Dianomic wind turbine demo of FogLAMP.
    Phidget based sensors:
        - Temperature & Humidity: HUM1000_0 (https://www.phidgets.com/?tier=3&catid=14&pcid=12&prodid=644)
        - Spatial: MOT1101_0 (https://www.phidgets.com/?tier=3&catid=10&pcid=8&prodid=975)
        - Rotary: 3531_0 (https://www.phidgets.com/?tier=3&catid=103&pcid=83&prodid=404)
        - Current: VCP1100_0 (https://www.phidgets.com/?tier=3&catid=16&pcid=14&prodid=983)
"""

import copy
import datetime
import logging
import math
import time 
import uuid 

from foglamp.common import logger
from foglamp.plugins.common import utils
from foglamp.services.south import exceptions

from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.CurrentInput import * 
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.Gyroscope import *
from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.Magnetometer import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *


__author__ = "Ori Shadmon" 
__copyright__ = "Copyright (c) 2019 Dianomic Systems Inc."
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_DEFAULT_CONFIG = {
    'plugin': {
        'description': 'Wind Turbine Poll Plugin',
        'type': 'string',
        'default': 'foglamp_phidget',
        'readonly': 'true'
    },
    'hubSN': {
        'description': 'VINT Hub Serial Number',
        'type': 'string',
        'default': '538854',
        'order': '1',
        'displayName': 'VINT Hub SN'
    },
    'assetPrefix': {
        'description': 'Prefix of asset name',
        'type': 'string',
        'default': 'foglamp_phidget/',
        'order': '2',
        'displayName': 'Asset Name Prefix'
    },
    'tempHumAssetName': {
        'description': 'Humidity/Temperature sensor asset name',
        'type': 'string',
        'default': 'weather',
        'order': '3',
        'displayName': 'Humidity/Temperature Asset Name'
    },
    'tempHumPort': {
        'description': 'VINT Hub port of temperature/humidity sensor',
        'type': 'string',
        'default': '0',
        'order': '4',
        'displayName': 'Humidity/Temperature Port'
    },
    'tempHumPoll': {
        'description': 'Obtain Humidity/Temperature every nth time the plugin is pulled', 
        'type': 'integer', 
        'default': '1',
        'order': '5', 
        'displayName': 'Humidity/Temperature Poll', 
    }, 
    'tempHumEnable': {
        'description': 'Enable Humidity/Temperature',
        'type': 'boolean', 
        'default': 'true', 
        'order': '6', 
        'displayName': 'Enable Humidity/Temperature'
    },
    'currentAssetName': {
        'description': 'Current sensor asset name',
        'type': 'string',
        'default': 'current',
        'order': '7',
        'displayName': 'Current Asset Name'
    },
    'currentPort': {
        'description': 'VINT Hub port of current sensor',
        'type': 'string',
        'default': '3',
        'order': '8',
        'displayName': 'Current Port'
    },
    'currentPoll': {
        'description': 'Obtain current every nth time the plugin is pulled', 
        'type': 'integer', 
        'default': '1', 
        'order': '9', 
        'displayName': 'Current Poll'
    },
    'currentEnable': {
        'description': 'Enable/Disable Current sensor', 
        'type': 'boolean',
        'default': 'true', 
        'order': '10', 
        'displayName': 'Enable Current'
    },
    'encoderAssetName': {
        'description': 'Encoder sensor asset name',
        'type': 'string',
        'default': 'encoder',
        'order': '11',
        'displayName': 'Encoder Asset Name'
    },
    'encoderPort': {
        'description': 'VINT Hub port of encoder sensor',
        'type': 'string',
        'default': '1',
        'order': '12',
        'displayName': 'Encoder Port'
    },
    'encoderPoll': {
        'description': 'Obtain encoder every nth time the plugin is pulled',
        'type': 'integer',
        'default': '1',
        'order': '13',
        'displayName': 'Encoder Poll'
    },
    'encoderEnable': {
        'description': 'Enable Encoder Sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '14',
        'displayName': 'Enable Encoder'
    },
    'spatialPort': {
        'description': 'VINT Hub port of spatial sensors', 
        'type': 'string', 
        'default': '2', 
        'order': '15', 
        'displayName': 'Spatial Port'
    },
    'accelerometerAssetName': {
        'description': 'accelerometer sensor asset name',
        'type': 'string',
        'default': 'accelerometer',
        'order': '16',
        'displayName': 'accelerometer Asset Name'
    },
    'accelerometerPoll': {
        'description': 'Obtain accelerometer every nth time the plugin is pulled',
        'type': 'integer',
        'default': '1',
        'order': '17',
        'displayName': 'Acceleration Poll'
    },
    'accelerometerEnable': {
        'description': 'Enable Acceleration Sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '18',
        'displayName': 'Acceleration Encoder'
    },
    'gyroscopeAssetName': {
        'description': 'gyroscope sensor asset name',
        'type': 'string',
        'default': 'gyroscope',
        'order': '19',
        'displayName': 'gyroscope Asset Name'
    },
    'gyroscopePoll': {
        'description': 'Obtain gyroscope every nth time the plugin is pulled',
        'type': 'integer',
        'default': '1',
        'order': '20',
        'displayName': 'Gyroscope Poll'
    },
    'gyroscopeEnable': {
        'description': 'Enable Gyroscope Sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '21',
        'displayName': 'Enable Gyroscope'
    },
    'magnetometerAssetName': {
        'description': 'magnetometer sensor asset name',
        'type': 'string',
        'default': 'magnetometer',
        'order': '22',
        'displayName': 'magnetometer Asset Name'
    },
    'magnetometerPoll': {
        'description': 'Obtain magnetometer every nth time the plugin is pulled',
        'type': 'integer',
        'default': '1',
        'order': '23',
        'displayName': 'Magnetometer Poll'
    },
    'magnetometerEnable': {
        'description': 'Enable Magnetometer Sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '24',
        'displayName': 'Enable Magnetometer'
    },
    'lightPort': {
        'description': 'VINT Hub port of light sensors', 
        'type': 'string',
        'default': '0',
        'order': '23',
        'displayName': 'Spatial Port'
    },
    'lightAssetName': {
        'description': 'light sensor asset name', 
        'type': 'string',
        'default': 'light',
        'order': '24',
        'displayName': 'light Asset Name'
    },
    'lightPoll': {
        'description': 'Obtain light every nth time the plugin is pulled',
        'type': 'integer',
        'default': '1',
        'order': '25',
        'displayName': 'Magnetometer Poll'
    },
    'lightEnable': {
        'description': 'Enable Magnetometer Sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '26',
        'displayName': 'Enable Magnetometer'
    },
    'soundPort': {
        'description': 'VINT Hub port of sound sensors', 
        'type': 'string',
        'default': '0',
        'order': '27',
        'displayName': 'Spatial Port'
    },
    'soundAssetName': {
        'description': 'sound sensor asset name', 
        'type': 'string',
        'default': 'sound',
        'order': '28',
        'displayName': 'sound Asset Name'
    },
    'soundPoll': {
        'description': 'Obtain sound every nth time the plugin is pulled',
        'type': 'integer',
        'default': '1',
        'order': '29',
        'displayName': 'Magnetometer Poll'
    },
    'soundEnable': {
        'description': 'Enable Magnetometer Sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '30',
        'displayName': 'Enable Magnetometer'
    }

}

_LOGGER = logger.setup(__name__, level=logging.INFO)


def plugin_info():
    """ Returns information about the plugin.
    Args:
    Returns:
        dict: plugin information
    Raises:
    """
    return {
        'name': 'foglamp_phidget Poll Plugin',
        'version': '1.0.0',
        'mode': 'poll',
        'type': 'south',
        'interface': '1.0',
        'config': _DEFAULT_CONFIG
    }


def plugin_init(config):
    """ Initialise the plugin.
    Args:
        config: JSON configuration document for the South plugin configuration category
    Returns:
        data: JSON object to be used in future calls to the plugin
    Raises:
    """
    try: 
        data = copy.deepcopy(config)
        if data['tempHumEnable']['value'] == 'true':
            data['humidity'] = HumiditySensor()
            data['humidity'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['humidity'].setHubPort(int(data['tempHumPort']['value']))
            data['humidity'].setIsHubPortDevice(False)
            data['humidity'].setChannel(0)
            data['humidity'].openWaitForAttachment(5000)
            try:
                data['humidity'].getHumidity()
            except Exception:
                pass

            data['temperature'] = TemperatureSensor()  
            data['temperature'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['temperature'].setHubPort(int(data['tempHumPort']['value']))
            data['temperature'].setIsHubPortDevice(False)
            data['temperature'].setChannel(0)
            data['temperature'].openWaitForAttachment(5000)
            try:
                data['temperature'].getTemperature()
            except Exception:
                pass

        if data['currentEnable']['value'] == 'true': 
            data['current'] = CurrentInput() 
            data['current'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['current'].setHubPort(int(data['currentPort']['value']))
            data['current'].setIsHubPortDevice(False)
            data['current'].setChannel(0)
            data['current'].openWaitForAttachment(5000)
            try:
                data['current'].getCurrent()
            except Exception:
                pass

        if data['encoderEnable']['value'] == 'true': 
            data['encoder'] = Encoder()
            data['encoder'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['encoder'].setHubPort(int(data['encoderPort']['value']))
            data['encoder'].setIsHubPortDevice(False)
            data['encoder'].setChannel(0)
            data['encoder'].openWaitForAttachment(5000)
            data['encoder'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    data['encoder'].getPosition()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break
    
        if data['accelerometerEnable']['value'] == 'true': 
            data['accelerometer'] = Accelerometer()
            data['accelerometer'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['accelerometer'].setHubPort(int(data['spatialPort']['value']))
            data['accelerometer'].setIsHubPortDevice(False)
            data['accelerometer'].setChannel(0)
            data['accelerometer'].openWaitForAttachment(5000)
            data['accelerometer'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    data['accelerometer'].getAcceleration()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break

        if data['gyroscopeEnable']['value'] == 'true': 
            data['gyroscope'] = Gyroscope()
            data['gyroscope'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['gyroscope'].setHubPort(int(data['spatialPort']['value']))
            data['gyroscope'].setIsHubPortDevice(False)
            data['gyroscope'].setChannel(0)
            data['gyroscope'].openWaitForAttachment(5000)
            data['gyroscope'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    data['gyroscope'].getAngularRate()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break

        if data['magnetometerEnable']['value'] == 'true': 
            data['magnetometer'] = Magnetometer()
            data['magnetometer'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['magnetometer'].setHubPort(int(data['spatialPort']['value']))
            data['magnetometer'].setIsHubPortDevice(False)
            data['magnetometer'].setChannel(0)
            data['magnetometer'].openWaitForAttachment(5000)
            data['magnetometer'].setDataInterval(20)
            i = 0 
            while i < 120: 
                try: 
                    data['magnetometer'].getMagneticField() 
                except Exception:
                    time.sleep(1)
                    i += 1
                else: 
                    break 

        if data['lightHumEnable']['value'] == 'true':
            data['light'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['light'].setHubPort(int(data['lightPort']['value']))
            data['light'].setIsHubPortDevice(False)
            data['light'].setChannel(0)
            i = 0 
            while i < 120: 
                try:
                    data['light'].getIlluminance() 
                except Exception: 
                    time.sleep(1) 
                    i += 1 
                else: 
                    break 

        if data['tempHumEnable']['value'] == 'true':
            data['sound'].setDeviceSerialNumber(int(data['hubSN']['value']))
            data['sound'].setHubPort(int(data['soundPort']['value']))
            data['sound'].setIsHubPortDevice(False)
            data['sound'].setChannel(0)
            i = 0
            while i < 120:
                try:
                    data['sound'].getdB()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break


    except Exception as ex:
        _LOGGER.exception("foglamp_phidget exception: {}".format(str(ex)))
        raise ex

    # counter to know when to run process 
    data['tempHumCount'] = 0 
    data['currentCount'] = 0 
    data['encoderCount'] = 0 
    data['accelerometerCount'] = 0 
    data['gyroscopeCount'] = 0 
    data['magnetometerCount'] = 0 
    data['lightCount'] = 0  
    data['soundCount'] = 0 

    # counter of last encoder value 
    data['encoderPreviousValue'] = 0
    data['encoderPreviousTime'] = 0  
    return data


def plugin_poll(handle):
    """ Extracts data from the sensor and returns it in a JSON document as a Python dict.
    Available for poll mode only.
    Args:
        handle: handle returned by the plugin initialisation call
    Returns:
        returns a sensor reading in a JSON document, as a Python dict, if it is available
        None - If no reading is available
    Raises:
        TimeoutError
    """
    # air quality is voltage reading between 0 and 5.1
    # we scale is to a value between 0 and 1023
    try:
        time_stamp = utils.local_timestamp()
        data = list()
        if handle['tempHumEnable']['value'] == 'true' and handle['tempHumCount'] == 0:
            data.append({
                'asset': '{}{}'.format(handle['assetPrefix']['value'], handle['tempHumAssetName']['value']),
                'timestamp': time_stamp,
                'key': str(uuid.uuid4()),
                'readings': {
                    "temperature": handle['temperature'].getTemperature(),
                    "humidity": handle['humidity'].getHumidity()
                }    
            })

        if handle['currentEnable']['value'] == 'true' and handle['currentCount'] == 0:
            data.append({
                'asset': '{}{}'.format(handle['assetPrefix']['value'], handle['currentAssetName']['value']),
                'timestamp': time_stamp,
                'key': str(uuid.uuid4()),
                'readings': {
                    "current": handle['current'].getCurrent()
                }
            })

        if handle['encoderEnable']['value'] == 'true' and handle['encoderCount'] == 0:
            value = handle['encoder'].getPosition()
            # convert time_stamp to be usable
            if ":" == time_stamp[-3:-2]:
                timestamp_new = datetime.datetime.strptime(time_stamp[:-3]+time_stamp[-2:], '%Y-%m-%d %H:%M:%S.%f%z')
            else: 
                timestamp_new = datetime.datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S.%f%z')

            if handle['encoderPreviousValue'] > 0:  # omit first one
                # calculate elapse time in milliseconds
                elapse_time = timestamp_new - handle['encoderPreviousTime']
                elapse_time = elapse_time.total_seconds()
                data.append({
                    'asset': '{}{}'.format(handle['assetPrefix']['value'], handle['encoderAssetName']['value']),
                    'timestamp': time_stamp,
                    'key': str(uuid.uuid4()),
                    'readings': {
                        # (current_total_iterations - previous_total_iterations) / (elapsed time in seconds) 
                        "rotation-per-second":  ((value - handle['encoderPreviousValue'])/1200)/elapse_time 
                    }
                })
            # update old values 
            handle['encoderPreviousValue'] = value 
            handle['encoderPreviousTime'] = timestamp_new 

        if handle['accelerometerEnable']['value'] == 'true' and handle['accelerometerCount'] == 0:
            x, y, z = handle['accelerometer'].getAcceleration()
            data.append({
                'asset': '{}{}'.format(handle['assetPrefix']['value'], handle['accelerometerAssetName']['value']),
                'timestamp': time_stamp,
                'key': str(uuid.uuid4()),
                'readings': {
                    "accelerometer-x": x,
                    "accelerometer-y": y, 
                    "accelerometer-z": z
                }
            })

        if handle['gyroscopeEnable']['value'] == 'true' and handle['gyroscopeCount'] == 0:
            x, y, z = handle['gyroscope'].getAngularRate()
            data.append({
                'asset': '{}{}'.format(handle['assetPrefix']['value'], handle['gyroscopeAssetName']['value']),
                'timestamp': time_stamp,
                'key': str(uuid.uuid4()),
                'readings': {
                    "gyroscope-x": x,
                    "gyroscope-y": y,
                    "gyroscope-z": z
                }
            })

        if handle['magnetometerEnable']['value'] == 'true' and handle['magnetometerCount'] == 0:
            x, y, z = handle['magnetometer'].getMagneticField()
            data.append({
                'asset': '{}{}'.format(handle['assetPrefix']['value'], handle['magnetometerAssetName']['value']),
                'timestamp': time_stamp,
                'key': str(uuid.uuid4()),
                'readings': {
                    "magnetometer-x": x,
                    "magnetometer-y": y,
                    "magnetometer-z": z
                }  
            })

        handle['tempHumCount'] = (handle['tempHumCount'] + 1) % int(handle['tempHumPoll']['value'])
        handle['currentCount'] = (handle['currentCount'] + 1) % int(handle['currentPoll']['value']) 
        handle['encoderCount'] = (handle['encoderCount'] + 1) % int(handle['encoderPoll']['value']) 
        handle['accelerometerCount'] = (handle['accelerometerCount'] + 1) % int(handle['accelerometerPoll']['value'])
        handle['gyroscopeCount'] = (handle['gyroscopeCount'] + 1) % int(handle['gyroscopePoll']['value'])
        handle['magnetometerCount'] = (handle['magnetometerCount'] + 1) % int(handle['magnetometerPoll']['value'])

    except (Exception, RuntimeError) as ex:
        _LOGGER.exception("foglamp_phidget exception: {}".format(str(ex)))
        raise exceptions.DataRetrievalError(ex)
    else:
        return data


def plugin_reconfigure(handle, new_config):
    """ Reconfigures the plugin

    Args:
        handle: handle returned by the plugin initialisation call
        new_config: JSON object representing the new configuration category for the category
    Returns:
        new_handle: new handle to be used in the future calls
    """
    _LOGGER.info("Old config for foglamp_phidget plugin {} \n new config {}".format(handle, new_config))
    # Shutdown sensors 
    try: 
        handle['humidity'].close() 
        handle['temperature'].close()
        handle['current'].close() 
        handle['encoder'].close() 
        handle['accelerometer'].close()  
        handle['gyroscope'].close() 
        handle['magnetometer'].close() 
    except Exception as ex:
        _LOGGER.exception("foglamp_phidget exception: {}".format(str(ex)))
        raise ex
    time.sleep(5) 
    new_handle = copy.deepcopy(new_config)
    try: 
        # check if temp/humidity sensor is enabled. If so restart it 
        if new_handle['tempHumEnable']['value'] == 'true': 
            new_handle['humidity'] = HumiditySensor()
            new_handle['humidity'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['humidity'].setHubPort(int(new_handle['tempHumPort']['value']))
            new_handle['humidity'].setIsHubPortDevice(False)
            new_handle['humidity'].setChannel(0)
            new_handle['humidity'].openWaitForAttachment(5000)
            try:
                new_handle['humidity'].getHumidity()
            except Exception:
                pass

            new_handle['temperature'] = TemperatureSensor()
            new_handle['temperature'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['temperature'].setHubPort(int(new_handle['tempHumPort']['value']))
            new_handle['temperature'].setIsHubPortDevice(False)
            new_handle['temperature'].setChannel(0)
            new_handle['temperature'].openWaitForAttachment(5000)
            try:
                new_handle['temperature'].getTemperature()
            except Exception:
                pass

        # check if current sensor is enabled, if so restart it 
        if new_handle['currentEnable']['value'] == 'true':
            new_handle['current'] = CurrentInput()
            new_handle['current'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['current'].setHubPort(int(new_handle['currentPort']['value']))
            new_handle['current'].setIsHubPortDevice(False)
            new_handle['current'].setChannel(0)
            new_handle['current'].openWaitForAttachment(5000)
            try:
                new_handle['current'].getCurrent()
            except Exception:
                pass

        # check if encoder sensor is enabled  
        if new_handle['encoderEnable']['value'] == 'true':
            new_handle['encoder'] = Encoder()
            new_handle['encoder'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['encoder'].setHubPort(int(new_handle['encoderPort']['value']))
            new_handle['encoder'].setIsHubPortDevice(False)
            new_handle['encoder'].setChannel(0)
            new_handle['encoder'].openWaitForAttachment(5000)
            new_handle['encoder'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    new_handle['encoder'].getPosition()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break

        # check if accelerometer is enabled
        if new_handle['accelerometerEnable']['value'] == 'true':
            new_handle['accelerometer'] = Accelerometer()
            new_handle['accelerometer'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['accelerometer'].setHubPort(int(new_handle['spatialPort']['value']))
            new_handle['accelerometer'].setIsHubPortDevice(False)
            new_handle['accelerometer'].setChannel(0)
            new_handle['accelerometer'].openWaitForAttachment(5000)
            new_handle['accelerometer'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    new_handle['accelerometer'].getAcceleration()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break
        # check if gyroscope is enabled 
        if new_handle['gyroscopeEnable']['value'] == 'true':
            new_handle['gyroscope'] = Gyroscope()
            new_handle['gyroscope'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['gyroscope'].setHubPort(int(new_handle['spatialPort']['value']))
            new_handle['gyroscope'].setIsHubPortDevice(False)
            new_handle['gyroscope'].setChannel(0)
            new_handle['gyroscope'].openWaitForAttachment(5000)
            new_handle['gyroscope'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    new_handle['gyroscope'].getAngularRate()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break
        # check if magnetometer enable is enabled 
        if new_handle['magnetometerEnable']['value'] == 'true':
            new_handle['magnetometer'] = Magnetometer()
            new_handle['magnetometer'].setDeviceSerialNumber(int(new_handle['hubSN']['value']))
            new_handle['magnetometer'].setHubPort(int(new_handle['spatialPort']['value']))
            new_handle['magnetometer'].setIsHubPortDevice(False)
            new_handle['magnetometer'].setChannel(0)
            new_handle['magnetometer'].openWaitForAttachment(5000)
            new_handle['magnetometer'].setDataInterval(20)
            i = 0
            while i < 120:
                try:
                    new_handle['magnetometer'].getMagneticField()
                except Exception:
                    time.sleep(1)
                    i += 1
                else:
                    break

        # check if hub has changed, if so init restart 
        if new_handle['hubSN']['value'] != handle['hubSN']['value']:
            new_handle['restart'] = 'yes'
        else:
            new_handle['restart'] = 'no'
    except Exception as ex:
        _LOGGER.exception("foglamp_phidget exception: {}".format(str(ex)))
        raise ex

    # counter to know when to run process
    new_handle['tempHumCount'] = 0
    new_handle['currentCount'] = 0
    new_handle['encoderCount'] = 0
    new_handle['accelerometerCount'] = 0
    new_handle['gyroscopeCount'] = 0
    new_handle['magnetometerCount'] = 0

    # counter of last encoder value
    new_handle['encoderPreviousValue'] = handle['encoderPreviousValue']

    return new_handle


def plugin_shutdown(handle):
    """ Shutdowns the plugin doing required cleanup, to be called prior to the South plugin service being shut down.

    Args:
        handle: handle returned by the plugin initialisation call
    Returns:
        plugin shutdown
    """
    try:
        handle['humidity'].close()
        handle['temperature'].close()
        handle['current'].close()
        handle['encoder'].close()
        handle['accelerometer'].close()
        handle['gyroscope'].close()
        handle['magnetometer'].close()
    except Exception as ex:
        _LOGGER.exception("foglamp_phidget exception: {}".format(str(ex)))
        raise ex
    _LOGGER.info('foglamp_phidget plugin shut down.')
