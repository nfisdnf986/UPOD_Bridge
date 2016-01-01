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

from GPS import Parser

global queue

BUFFSIZE = 1000
queue = Queue.Queue(BUFFSIZE)


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
        self.log = logging.getLogger(__name__)

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
        print 'Processing -->', data
        self.log.info('Processing {data}'.format(data=data))

        # c = Parser.parse(data)

        # print 'UTC Time:', c.Utc
        # print 'Latitute:', c.Latitute
        # print 'Longitude:', c.Longitude
        # print 'FixQuality:', c.FixQuality
        # print 'Satellites:', c.Satellites
        # print 'Dilution:', c.Dilution
        # print 'Altitude:', c.Altitude
        # print 'Height:', c.Height
        # print 'Since DGPS update:', c.DGPS_update
        # print 'DGPS station Id:', c.DGPS_Id
