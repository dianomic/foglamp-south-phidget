# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: https://foglamp-foglamp-documentation.readthedocs-hosted.com
# FOGLAMP_END

""" Module for Phidget poll mode plugin

    The following is intended as the south service plugin of Dianomic phidget demo of FogLAMP.
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
import json

from foglamp.plugins.south.phidget import wrapper
from foglamp.common import logger
from foglamp.plugins.common import utils
from foglamp.services.south import exceptions

__author__ = "Ori Shadmon" 
__copyright__ = "Copyright (c) 2019 Dianomic Systems Inc."
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_DEFAULT_CONFIG = {
    'plugin': {
        'description': 'FogLAMP Phidget Poll Plugin',
        'type': 'string',
        'default': 'phidget',
        'readonly': 'true'
    },
    'assetPrefix': {
        'description': 'Prefix of asset name',
        'type': 'string',
        'default': 'phidget_',
        'order': '1',
        'displayName': 'Asset Name Prefix'
    },
    'mapping': {
        'description': 'Phidget Mapping',
        'type': 'JSON',
        'default': '{"values":[{"hubSN":538395,"port":0,"sensorType":"TemperatureSensor","assetName":"weather","poll":1},{"hubSN":538395,"port":0,"sensorType":"HumiditySensor","assetName":"weather","poll":1},{"hubSN":538395,"port":1,"sensorType":"LightSensor","assetName":"light","poll":1},{"hubSN":538395,"port":2,"sensorType":"SoundSensor","assetName":"sound","poll":1}]}',
        'order': '2',
        'displayName': 'Phidget Map'
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
        'name': 'phidget Poll Plugin',
        'version': '2.4.0',
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
        sensors = []
        _LOGGER.info(data['mapping'])
        d = data['mapping']['value']
        if "values" in d:
            if isinstance(d["values"], list):
                for entry in d["values"]:
                    if isinstance(entry, dict):
                        if "hubSN" in entry and isinstance(entry["hubSN"],int) and \
                                "port" in entry and isinstance(entry["port"],int) and \
                                "sensorType" in entry and isinstance(entry["sensorType"],str) and \
                                "poll" in entry and isinstance(entry["poll"],int) and \
                                "assetName" in entry and isinstance(entry["assetName"],str):
                            sensors.append(getattr(wrapper, entry["sensorType"] + "Wrapper")(entry))
                    else:
                        print('Error: entry in list must be a dictionary')
            else:
                print('Error: "values" does not point to a list')
        else:
            print('Error: no "values" key')
        data['sensors'] = sensors
    except Exception as ex:
        _LOGGER.exception("phidget exception: {}".format(str(ex)))
        raise ex

    # counter to know when to run process 
    data['tempHumCount'] = 0 
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
    data = {}
    time_stamp = utils.local_timestamp()
    for sensor in handle['sensors']:
        if sensor.count == 0:
            try:
                readings = sensor.get_reading()
                if readings is not None:
                    if sensor.assetName in data:
                        data[sensor.assetName]['readings'] = {**data[sensor.assetName]['readings'], **readings}
                    else:
                        data[sensor.assetName] = {
                            'asset': '{}{}'.format(handle['assetPrefix']['value'], sensor.assetName),
                            'timestamp': time_stamp,
                            'key': str(uuid.uuid4()),
                            'readings': readings
                        }
            except (Exception, RuntimeError) as ex:
                _LOGGER.exception("phidget exception: {}".format(str(ex)))
        sensor.count = (sensor.count + 1) % sensor.poll
    return list(data.values())


def plugin_reconfigure(handle, new_config):
    """ Reconfigures the plugin

    Args:
        handle: handle returned by the plugin initialisation call
        new_config: JSON object representing the new configuration category for the category
    Returns:
        new_handle: new handle to be used in the future calls
    """
    _LOGGER.info("Old config for phidget plugin {} \n new config {}".format(handle, new_config))
    # for sensor in handle['sensors']:
    #     sensor.close()
    # return plugin_init(new_config)
    for key in new_config:
        handle[key] = new_config[key]
    return handle


def plugin_shutdown(handle):
    """ Shutdowns the plugin doing required cleanup, to be called prior to the South plugin service being shut down.

    Args:
        handle: handle returned by the plugin initialisation call
    Returns:
        plugin shutdown
    """
    for sensor in handle['sensors']:
        sensor.close()
    _LOGGER.info('phidget plugin shut down.')


