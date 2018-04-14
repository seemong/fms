from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import os
import numpy
import re
import pdb
from osgeo import gdal

SECONDSPERDEGREE = 3600

class HgtFile(object):
    """
    Implements a generic HGT file.
    """
    def __init__(self, filename):
        self._filename = filename
        if re.search(r'\.hgt$', filename) != None:
            self._init_hgt(filename)
        elif re.search(r'\.tif$', filename) != None:
            self._init_tif(filename)
        else:
            raise Exception('not a HGT or TIF file')
        
    def _init_hgt(self, filename):
        """
        Init a HGT file. All HGT files are square and 
        have an arc of 1 second
        """
        stat = os.stat(filename)
        size = stat.st_size
        if size == 1201 * 1201 * 2:
            self._arc = 3
        elif size == 3601 * 3601 * 2:
            self._arc = 1
        else:
            raise Exception('HGT file is not 1 or 3 arc seconds')
    
        self._xincrement = 1.0/(SECONDSPERDEGREE/self._arc)
        self._yincrement = self._xincrement
        self._rows = self._cols = SECONDSPERDEGREE/self._arc + 1
        
        basename = os.path.basename(filename)
        self._xbot, self._ybot, self._xtop, self._ytop= \
            HgtFile._parseHgtFilename(basename)
            
        data = numpy.fromfile(self._filename, dtype=">i2")
        self._zs = \
            data.reshape(self._rows, self._cols).astype("float32")
            
    def _init_tif(self, filename):
        """
        Init a tif file using gdal. Metadata indicates the 
        extent of the data.
        """
        g = gdal.Open(sys.argv[1])
        self._cols = g.RasterXSize
        self._rows = g.RasterYSize
        count = g.RasterCount
        gt = g.GetGeoTransform()
        self._xtop = gt[0]
        self._xincrement = gt[1]
    
        self._ytop = gt[3]
        self._yincrement = -gt[5]
        
        self._xbot = self._xtop * self._xincrement * (self._cols - 1)
        self._ybot = self._ytop * self._yincrement * (self._rows - 1)
    
        self._zs = g.ReadAsArray()
               
    @classmethod
    def _parseHgtFilename(cls, filename):
        """
        The filename implicitly defines the southwest coordinates
        Split out filename and get lower left lon and lat and 
        upper left and upper right.
        The top corner is 1 minute away in both directions
        """
        # do north/south
        ns = filename[0:1]
        lat = float(filename[1:3])
        if ns.lower() == 's':
            lat = -lat
        
        # do east west
        ew = filename[3:4]
        lon = float(filename[4:7])
        if ew.lower() == 'w':
            lon = -lon
        
        return lon, lat, lon + 1, lat + 1
        
    def get_arc(self):
        """Return how many seconds of arc for this file"""
        return _self.arc
        
    def get_xbottom(self):
        """Return lat coordinates of southwest corner"""
        return self._xbottom
        
    def get_ybottom(self):
        """Return lon coordinates of southwest corner"""
        return self._ybottom
        
    def get_extent(self):
        """Return bottom, left, top, right"""
        return self._xbottom, self._ybottom, \
            self._xtop, self._ytop
        
    def get_x_increment(self):
        """Return the x increment for each z data point"""
        return self._xincrement
        
    def get_y_increment(self):
        """Return the x increment for each z data point"""
        return self._yincrement
        
    def get_cols(self):
        """How many cols there are in the data file"""
        return _self._cols
        
    def get_rows(self):
        """How many rows there are in the data file"""
        return self._rows
        
    def get_zs(self):
        """
        Return the z data table, with the data in English reading order.
        The table is a two dimensional 
        numpy array, going from north to south for each row.
        Within each column, it goes from west to east
        """
        return self._z
        
    def _get_indices(self, x, y):
        """Helper method: return x and y indices for the given coords"""
        xindex = int((x - self._xtop)/self._xincrement)
        yindex = int((y - self._xtop)/self._yincrement)
        return xindex, yindex
        
    def get_z(self, x, y):
        """Return z at given x and y"""
        xindex, yindex = self._get_indices(x, y)
        return self._zs[xindex, yindex]
        
    def get_zslice(self, left, bottom, top, right):
        """
        Return a slice of the data array corresponding to the
        bounding box given of left, bottom, top, right
        Raises an index out of bounds error if the bounds are too large
        """
        xb, yb = self._get_indices(left, bottom)
        xt, yt = self._get_indices(top, right)
        return self._zs[xt:xb+1,yt:yb+1]
        
    def __str__(self):
        return '{0}: rows({1}), cols({2}), topx({3}), topy({4}), '  \
            'botx({5}), boty({6}), xincr({7}), yincr({8})'        \
            .format(os.path.basename(self._filename), self._rows, \
                self._cols, self._xtop, self._ytop, self._xbot,   \
                self._ybot, self._xincrement, self._yincrement)
        
if __name__ == '__main__':
    # hgtf = Hgt3File(sys.argv[1])
    f = HgtFile(sys.argv[1])
    print(f)
    s = f.get_zslice(-121.56, 46.74, -121.21, 46.9)
    print(s)

    

    

    
