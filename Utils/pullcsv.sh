#!/bin/bash
# Copyright (C) 2016 Arduino UPOD
# Author: Sunil <suba5417@colorado.edu>

# sshpass to copy without entering the pasword
# Remove sshpass if security is a concern
sshpass -p 'arduino' scp root@arduino.local:/mnt/sda1/arduino/* ~/logs/
