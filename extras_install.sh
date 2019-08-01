#!/usr/bin/env bash

#    Copyright (c) 2019 Dianomic Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        https://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

##
## Author: Amandeep Singh Arora
##

set -e

rm -rf /tmp/foglamp-phidget-install
mkdir /tmp/foglamp-phidget-install
cd /tmp/foglamp-phidget-install
wget https://www.phidgets.com/downloads/phidget22/libraries/linux/libphidget22.tar.gz
tar -xzvf libphidget22.tar.gz
cd libphidget22-*
./configure --prefix=/ && make && make install
fn=`find -name *libphidget22.rule*`
mv `find -name *libphidget22.rule*` /etc/udev/rules.d/.
cd
rm -rf /tmp/foglamp-phidget-install

