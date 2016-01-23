"""
Abstract class for Db classes
"""

from abc import ABCMeta, abstractmethod

class AbstractDb(object):
    """ AbstractDb """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def query(self, condition):
        pass

    @abstractmethod
    def read(self, query):
        pass
