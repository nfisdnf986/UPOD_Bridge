#!/usr/bin/python

"""
DataProcessor.py

Get data from the queue and process it.
"""

import Queue
import threading
import logging

global data_queue

BUFFSIZE = 100
data_queue = Queue.Queue(BUFFSIZE)

# log = logging.getLogger(__name__)

class DataProcessor(threading.Thread):
    """
    Data processor
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(DataProcessor,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        # get data and process it
        while True:
            data = data_queue.get()
            # log.info(data)
            print 'Data Processor --> ', data
        return
