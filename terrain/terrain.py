from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import os
import numpy
import srtm 
import hgt

class Terrain(object):
    """
    A terrain object presents an abstract interface to a set of
    terrain digital elevation files
    """
    
    def __init__(self):
        self._directories = []
        self._hgtFiles = []

if __name__ == '__main__':
    terrain = Terrain()
    terrain.add_data('data/hgt15')
    
