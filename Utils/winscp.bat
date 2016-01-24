:: Copyright (C) 2016 Arduino UPOD
:: Version: 0.2.0
:: Author: Sunil <suba5417@colorado.edu>

@ECHO OFF

::
:: Usage: Double click on the bat/exe file
::
:: Prequisities: make sure windows is connected to
::   arduino_09XXXX wifi
::

:: stop gap for arduino yun unable to connect to the "UCB Wirless" wifi
:: http://www.hanselman.com/blog/HowToConnectToAWirelessWIFINetworkFromTheCommandLineInWindows7.aspx
:: connect to Arduino_09XXX wifi 
REM netsh wlan connect name=wifi_name_here

:: Set the log folder to copy the csv and log files
set ARDUINO_FOLDER = "C:\arduino"

if not exist %ARDUINO_FOLDER% (
   mkdir %ARDUINO_FOLDER%
)

::
:: Pull the CSV file from arduino yun to windows LOG_FOLDER
::
pscp -pw arduino root@arduino.local:/mnt/sda1/* %ARDUINO_FOLDER%

echo File copied to %ARDUINO_FOLDER% successfully
pause

:: Disconnect from Arduino wifi
REM netsh wlan disconnect

:: re-connect to original wifi 
REM netsh wlan connect name=wifi_name_here

@ECHO ON
