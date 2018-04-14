from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import os
import numpy
import pdb

SECONDSPERDEGREE = 3600

class HgtFile(object):
    """
    Implements a generic HGT file.
    """
    def __init__(self, filename, arc):
        self._filename = filename
        self._arc = arc
        self._increment = 1/(SECONDSPERDEGREE/arc)
        self._across = SECONDSPERDEGREE/arc + 1
        
        basename = os.path.basename(filename)
        self._xllcorner, self._yllcorner = \
            HgtFile._parseFilename(basename)
            
        data = numpy.fromfile(self._filename, dtype=">i2")
        self._zs = \
            data.reshape(self._across, self._across).astype("float32")
        
    @classmethod
    def _parseFilename(cls, filename):
        """Split out filename and get lower left lon and lat"""
        ns = filename[0:1]
        lat = float(filename[1:3])
        if ns.lower() == 's':
            lat = -lat
        
        ew = filename[3:4]
        lon = float(filename[4:7])
        if ew.lower() == 'w':
            lon = -lon
        
        return lon, lat
        
    def get_arc(self):
        """Return how many seconds of arc for this file"""
        return _self.arc
        
    def get_xllcorner(self):
        """Return lat coordinates of southwest corner"""
        return self._xllcorner
        
    def get_yllcorner(self):
        """Return lon coordinates of southwest corner"""
        return self._yllcorner
        
    def get_extent(self):
        """Return bottom, left, top, right"""
        return self._xllcorner, self._yllcorner, \
            self._xllcorner + 1, self_yllcorner + 1
        
    def get_increment(self):
        """Return increment for each z data point"""
        return self._increment
        
    def get_across(self):
        """How many rows there are in the data file"""
        return _self._across
        
    def get_num_cols(self):
        """HGT files have same number of rows and columns"""
        return self.get_num_rows()
        
    def get_zs(self):
        """
        Return the z data table, with the data in English reading order.
        The table is a two dimensional 
        numpy array, going from north to south for each row.
        Within each column, it goes from west to east
        """
        return self._z
        
    def get_z(self, lon, lat):
        """Return z at lon and lat"""
        pass
        
class Hgt3File(HgtFile):
    def __init__(self, filename):
        super().__init__(filename, 3)

    
    
if __name__ == '__main__':
    hgtf = Hgt3File(sys.argv[1])

