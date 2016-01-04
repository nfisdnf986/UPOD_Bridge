"""
SensorData.py

Parse the ATMega data string into converted Sensor data object
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "suba5417@colorado.edu"

import logging
from GPS import Parser

log = logging.getLogger(__name__)

MICROVOLTS_PER_BIT = .1875

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

        self.Quad_Aux1 = self._get_QuatStat_value([8])
        self.Quad_Aux2 = self._get_QuatStat_value(tokens[10])
        self.Quad_Aux3 = self._get_QuatStat_value(tokens[12])
        self.Quad_Aux4 = self._get_QuatStat_value(tokens[14])

        self.Quad_Main1 = self._get_QuatStat_value(tokens[9])
        self.Quad_Main2 = self._get_QuatStat_value(tokens[11])
        self.Quad_Main3 = self._get_QuatStat_value(tokens[13])
        self.Quad_Main4 = self._get_QuatStat_value(tokens[15])

        self.Fig210_Heat = self._get_ADC_value(tokens[16])
        self.Fig210_Sens = self._get_ADC_value(tokens[17])
        self.Fig280_Heat =  self._get_ADC_value(tokens[18])
        self.Fig280_Sens = self._get_ADC_value(tokens[19])
        self.BL_Mocoon_Sens = self._get_ADC_value(tokens[20])
        self.Adc2_Channel_2 = self._get_ADC_value(tokens[21])
        self.E2VO3_Heat = self_get_ADC_value(tokens[22])
        self.E2VO3_Sens = self._get_ADC_value(tokens[23])
        self.GpsData = self._get_gps_data(tokens[24])

    def _get_gps_data(self, gps_data):
        if not gps_data:
            log.error('Gps data is empty. GPS signal is weak maybe!')
            return None

        gps = Parser.parse(gps_tokens)
        return gps

    def _get_QuatStat_value(self, data):
        if not data:
            log.error('QuatStat value is empty')
            return None

        return float(data)

    def _get_ADC_value(self, data):
        if not data:
            log.error('ADC value is empty!')
            return None

        return float(data) * MICROVOLTS_PER_BIT
