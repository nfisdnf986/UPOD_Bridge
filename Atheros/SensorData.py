"""
SensorData.py
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "suba5417@colorado.edu"

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
