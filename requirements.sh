#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2019 Dianomic Systems Inc.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##--------------------------------------------------------------------

##
## Author: Ori Shadmon 
##

set -e

# Apt package
sudo apt-get install libusb-1.0-0-dev

mkdir /tmp/wind-turbine-install
cd /tmp/wind-turbine-install

# Linux specific prerequisites - https://www.phidgets.com/docs/OS_-_Linux
wget https://www.phidgets.com/downloads/phidget22/libraries/linux/libphidget22.tar.gz
tar -xzvf /tmp/wind-turbine-install/libphidget22.tar.gz
cd /tmp/wind-turbine-install/libphidget22-*
./configure --prefix=/ && make && sudo make install
fn=`find -name *libphidget22.rule*`
sudo mv ${fn} /etc/udev/rules.d.

# Python3 specific prerequisites - https://www.phidgets.com/docs/Language_-_Python 
pip3 install -Ir python/requirements-foglamp_phidget.txt --no-cache-dir

sudo rm -rf /tmp/wind-turbine-install
