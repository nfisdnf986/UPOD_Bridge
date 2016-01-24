#!/bin/bash
# Copyright (C) 2016 Arduino UPOD
# Author: Sunil <suba5417@colorado.edu>

# copy the new python source files to the arduino

# sshpass to copy without entering the pasword
# Remove sshpass if security is a concern
sshpass -p 'arduino' scp /home/sunny/prv/github/UPOD_Bridge/Atheros/* root@arduino.local:/root/

# copy GPS module sources
sshpass -p 'arduino' scp /home/sunny/prv/github/UPOD_Bridge/Atheros/GPS/* root@arduino.local:/root/GPS/

