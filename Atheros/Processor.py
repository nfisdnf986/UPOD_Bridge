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
from CsvWriter import CsvWriter
# from pprint import pprint

global queue

log = logging.getLogger(__name__)


BUFFSIZE = 1000
queue = Queue.Queue(BUFFSIZE)
DELIMITER = '#'


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
        self.CsvFileCreated = False
        self.file = None

    def run(self):
        # get data and process it
        while True:
            # wait for the data to be put in queue
            # if queue is empty. Otherwise process queue
            if queue.empty():
                self.event.wait()

            data = queue.get()
            
            # Stop gap fix for csv writer
            if not self.CsvFileCreated:
                self.file = CsvWriter(datetime.fromtimestamp(float(data[0])).strftime('UPODXX%d%m%y.csv'))
                self.CsvFileCreated = True

            self.process(data)

    def process(self, data):
        # avoid processing empty data
        if not data:
            return

        log.info('Processing {data}'.format(data=data))
        print data
        tokens = data.split(DELIMITER)
        sensor_data = SensorData(tokens)
        # pprint(vars(sensor_data))
        # pprint(vars(sensor_data.GpsData))

        self.file.write_sensor_data(sensor_data)
