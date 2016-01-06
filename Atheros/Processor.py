"""
DataProcessor.py

Get data from the queue and process it.
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "suba5417@colorado.edu"


import Queue
import threading
import logging
import time

from datetime import datetime
from SensorData import SensorData
from CsvWriter import RotatingCsvWriter
# from pprint import pprint

global queue

log = logging.getLogger(__name__)


BUFFSIZE = 1000
queue = Queue.Queue(BUFFSIZE)
DELIMITER = '#'
DATE_TIME = 0

class DataProcessor(threading.Thread):
    """
    Data processor
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, event=None):
        super(DataProcessor,self).__init__()
        self.target = target
        self.name = name
        self.setDaemon(True)
        self.event = event
        self._file = None

    def run(self):
        # get data and process it
        while True:
            # wait for the data to be put in queue
            # if queue is empty. Otherwise process queue
            if queue.empty():
                self.event.wait()

            data = queue.get()
            self.process(data)

    def process(self, data):
        # avoid processing empty data
        if not data:
            return

        log.info('Processing {data}'.format(data=data))
        print data
        tokens = data.split(DELIMITER)
        sensor_data = SensorData(tokens)

        # if file not created then create it.
        # Stop gap fix for date & time not set in Atheros
        # Sync the time between Atheros and ATMega
        # UPODXX... xx has to be replaced with POD serial number
        if not self._file:
            dt = float(tokens[DATE_TIME])
            # sychronize Atheros system clock with ATMega
            sync_datetime(dt)
            self._file = RotatingCsvWriter(datetime.fromtimestamp(dt)
                                             .strftime('/mnt/sda1/UPODXX%d%m%y.csv'))

        # pprint(vars(sensor_data))
        # pprint(vars(sensor_data.GpsData))

        self._file.write(sensor_data)

    def sync_datetime(self, dt):
        import os
        # see if i need to set hardware clock or system clock
        os.system('date -s "{datetime}"'.format(datetime=dt))
