"""
SensorData.py
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "suba5417@colorado.edu"

import datetime

class SensorData(object):
    def __init__(self, tokens):
        self.RtcDate = None
        self.RtcTime = None
        self.BmpTemperature = None
        self.BmpPressure = None
        self.ShtTemperature = None
        self.ShtPressure = None
        self.CO2 = None
        self.WindSpeed = None
        self.WindDirection = None
        self.Quad_Aux1 = None
        self.Quad_Aux2 = None
        self.Quad_Aux3 = None
        self.Quad_Aux4 = None
        self.Quad_Main1 = None
        self.Quad_Main2 = None
        self.Quad_Main3 = None
        self.Quad_Main4 = None
        # self.Fig210_Heat_ADC = None
        self.Fig210_Heat = None
        # self.Fig210_Sens_ADC = None
        self.Fig210_Sens = None
        self.Fig280_Heat =  None
        self.Fig280_Sens = None
        self.BL_Mocoon_Sens = None
        self.Adc2_Channel_2 = None
        self.E2VO3_Heat = None
        self.E2VO3_Sens = None
        self.GpsTime = None
        self.GpsDate = None
        self.LatitudeCoord = None
        self.LatitudeNS = None
        self.LongitudeCoord = None
def ConvertUnixToUTC(RTC_token):
    return datetime.datetime.fromtimestamp(RTC_token).strftime('%Y-%m-%d, %H:%M:%S')

def ConvertWindDirection(WindDirectionToken):
    # The following table is ADC readings for the wind direction sensor output, sorted from low to high.
	# Each threshold is the midpoint between adjacent headings. The output is degrees for that ADC reading.
	# Note that these are not in compass degree order! See Weather Meters datasheet for more information.
    if adc < 380:
        return 113
    if adc < 393:
        return 68
	if adc < 414:
        return 90
	if adc < 456:
        return 158
	if adc < 508:
        return 135
	if adc < 551:
        return 203
	if adc < 615:
        return 180
	if adc < 680:
        return 23
	if adc < 746:
        return 45
	if adc < 801:
        return 248
	if adc < 833:
        return 225
	if adc < 878:
        return 338
	if adc < 913:
        return 0
	if adc < 940:
        return 293
	if adc < 967:
        return 315
    if adc < 990:
        return 270
    else:
        return -1; #error, disconnected?
