from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import os
import numpy
import pdb

class HgtFile(object):
    """
    Implements a generic HGT file.
    """
    def __init__(self, filename, arc):
        self._filename = filename
        self._arc = arc
        
        basename = os.path.basename(filename)
        self._xllcorner, self._yllcorner = \
            HgtFile._parseFilename(basename)
            
        data = numpy.fromfile(self._filename, dtype=">i2")
        num_across = self.get_num_rows()
        self._zs = \
            data.reshape(num_across, num_across).astype("float32")
        
    @classmethod
    def _parseFilename(cls, filename):
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
        return _self.arc
        
    def get_xllcorner(self):
        return self._xllcorner
        
    def get_yllcorner(self):
        return self._yllcorner
        
    def get_increment(self):
        return 1.0 / (3600 / self._arc)
        
    def get_num_rows(self):
        return 3600/self._arc + 1
        
    def get_num_cols(self):
        return self.get_num_rows()
        
    def get_zs(self):
        return self._z
        
    def get_z(self, lon, lat):
        """Return z at lon and lat"""
        pass
        
class Hgt3File(HgtFile):
    def __init__(self, filename):
        super().__init__(filename, 3)

    
    
if __name__ == '__main__':
    hgtf = Hgt3File(sys.argv[1])

