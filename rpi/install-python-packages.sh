#!/bin/bash

echo "Install pre-requisite Python packages needed to run programs"
echo "under the Raspbian operating system on Raspberry Pi."

echo "Installing 'python-pip'"
sudo apt-get install python-pip

echo "'Installing RPi.GPIO'"
sudo pip install RPi.GPIO

echo "Installing 'requests'"
sudo pip install requests

