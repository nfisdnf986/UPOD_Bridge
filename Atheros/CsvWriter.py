"""
CsvWriter.py

"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "suba5417@colorado.edu"

import csv

class CsvWriter(object):
    write_header = True
    
    def __init__(self, filename):
        self.header = ('Rtc Date', 'Rtc Time', 'BMP Temp(C)', 'BMP Pres(mb)',
                       'SHT25 Temp(C)', 'SHT25 Humidity', 'CO2(ADC VAL)', 'Wind Speed(mph)',
                       'Wind Direction(deg)', 'Quad-Aux-1(microVolts)', 'Quad-Main-1(microVolts)',
                       'Quad-Aux-2(microVolts)','Quad-Main-2(microVolts)', 'Quad-Aux-3(microVolts)',
                       'Quad-Main-3(microVolts)', 'Quad-Aux-4(microVolts)', 'Quad-Main-4(microVolts)',
                       'Fig 210 Heat(milliVolts)', 'Fig 210 Sens(milliVolts)',
                       'Fig 280 Heat(milliVolts)', 'Fig 280 Sens(milliVolts)', 'BL Moccon sens(milliVolts)',
                       'ADC2 Channel-2(empty)', 'E2VO3 Heat(milliVolts)', 'E2VO3 Sens(milliVolts)',
                       'GPS Date', 'GPS Time(UTC)', 'Latitude','Longitude',
                       'Fix Quality', 'Altitude(meters above sea level)', 'Statellites')
        self.file = open(filename, 'a')
        self.writer = csv.writer(self.file)
        self.writer.writerow(self.header)

    def write_sensor_data(self, sensor):
        try:
            self.writer.writerow((sensor.RtcDate,
                            sensor.RtcTime,
                            sensor.BmpTemperature,
                            sensor.BmpPressure,
                            sensor.Sht25Temperature,
                            sensor.Sht25Humidity,
                            sensor.CO2,
                            sensor.WindSpeed,
                            sensor.WindDirection,
                            sensor.Quad_Aux1,
                            sensor.Quad_Main1,
                            sensor.Quad_Aux2,
                            sensor.Quad_Main2,
                            sensor.Quad_Aux3,
                            sensor.Quad_Main3,
                            sensor.Quad_Aux4,
                            sensor.Quad_Main4,
                            sensor.Fig210_Heat,
                            sensor.Fig210_Sens,
                            sensor.Fig280_Heat,
                            sensor.Fig280_Sens,
                            sensor.BL_Mocon_Sens,
                            sensor.Adc2_Channel_2,
                            sensor.E2VO3_Heat,
                            sensor.E2VO3_Sens,
                            sensor.GpsData.UtcDate,
                            sensor.GpsData.UtcTime,
                            sensor.GpsData.Latitude,
                            sensor.GpsData.Longitude,
                            sensor.GpsData.FixQuality,
                            sensor.GpsData.Altitude,
                            sensor.GpsData.Satellites))
        finally:
            self.file.flush()
