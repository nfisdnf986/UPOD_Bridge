#!/usr/bin/python

"""
server.py

Read the data from the ATMega and post to processing Queue thread
"""

import sys
import os

# import path
sys.path.insert(0, '/usr/lib/python2.7/bridge')  

import logging
import Queue
import time

from Processor import DataProcessor, data_queue
from threading import current_thread
from bridgeclient import BridgeClient as bridgeclient

# setup logging
# set up the logging
# print('Setting up logging module...')
# basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
# logging.config.fileConfig('%s/logging.conf' % basepath)
# log = logging.getLogger(__name__)


def main(*argv):
    # setup data processing thread
    processor = DataProcessor(name='DataProcessor-Thread')
    processor.start()
    
    channel = bridgeclient()
    
    last_seen = ''
    # Get data from the Tx-channel and post it the queue
    while True:
        data = channel.get('TX-channel')
        if data == last_seen:
            continue

        data_queue.put(data)
        time.sleep(.7)


if __name__ == '__main__':
    current_thread().name = 'Server-Thread'
    main(sys.argv)
