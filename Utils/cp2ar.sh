#!/bin/bash

# copy the new python source files to the arduino
scp /home/sunny/prv/github/UPOD_Bridge/Atheros/* root@arduino.local:/root/

# copy GPS module sources
scp /home/sunny/prv/github/UPOD_Bridge/Atheros/GPS/* root@arduino.local:/root/GPS/

