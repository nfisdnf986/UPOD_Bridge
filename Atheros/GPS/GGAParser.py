""" 
GGAParser.py 

Represents the global positioning system fix data
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "suba5417@colorado.edu"


import logging

class GGAParser(object):
    """ 
    Global Positioning System Fix Data
    """
    def __init__(self):
        self.log = logging.getLogger(__name__)
        # Fix taken at UTC
        self.Utc = None
        
        self.Latitute = None
        self.Longitude = None

        # Fix quality:
        # 0 = invalid
        # 1 = GPS fix (SPS)
        # 2 = DGPS fix
        # 3 = PPS fix
        # 4 = Real Time Kinematic
        # 5 = Float RTK
        # 6 = estimated (dead reckoning) (2.3 feature)
        # 7 = Manual input mode
        # 8 = Simulation mode
        self.FixQuality = None

        # Number of satellites being tracked
        self.Satellites = None
        # Horizontal dilution of position
        self.Dilution = None
        # Altitude, Meters, above mean sea level
        self.Altitude = None
        # Height of geoid (mean sea level) above WGS84 ellipsoid
        self.Height = None
        # time in seconds since last DGPS update
        self.DGPS_update = None
        # DGPS station ID number
        self.DGPS_Id = None

    def _get_utc(self, data):
        number = int(data)
        utc = ''
        return data

    def _get_latitide(self, data, direction):
        return data + " "+ direction

    def _get_longitude(self, data, direction):
        return data + " " + direction

    def _get_fixquality(self, data):
        return data

    def _get_satellites(self, data):
        return data

    def _get_dilution(self, data):
        return data

    def _get_altitude(self, data, direction):
        return data + " " + direction

    def _get_height(self, data, direction):
        return data + " " + direction

    def _get_DGPS_update(self, data):
        pass

    def _get_DGPS_Id(self, data):
        pass

    def parse(self, gpsdata):
        tokens = gpsdata.split(',')
        self.log.info(len(tokens))
        self.log.info('GGA parsing string = {data}'.format(data = tokens))
        self.Utc = self._get_utc(tokens[1])
        self.Latitute = self._get_latitide(tokens[2], tokens[3])
        self.Longitude = self._get_longitude(tokens[4], tokens[5])
        self.FixQuality = self._get_fixquality(tokens[6])
        self.Satellites = self._get_satellites(tokens[7])
        self.Dilution = self._get_dilution(tokens[8])
        self.Altitude = self._get_altitude(tokens[9], tokens[10])
        self.Height = self._get_height(tokens[11],  tokens[12])
        self.DGPS_update = self._get_DGPS_update(tokens[13])
        self.DGPS_Id = self._get_DGPS_Id(tokens[14])
        # checksum = tokens[15]
