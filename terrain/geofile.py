from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import os
import numpy
import re
from osgeo import gdal

SECONDSPERDEGREE = 3600

class GeoFile(object):
    """
    Implements a an abstract Geo file representing either
    hgt, tif or esri formats.
    """
    def __init__(self, filename):
        self._filename = filename     
        
        # these values initialized by concrete subclass  
        self._rows = 0
        self._cols = 0
        self._xincrement = 0
        self._yincrement = 0
        self._xbot = 0
        self._ybot = 0
        self._xtop = 0
        self._ytop = 0
        # no data -- read only on request
        self_zs = None
        
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
        
    def read_data(self):
        """
        This function reads from the abstracted file depending on
        the file type.
        Return the z data table, with the data in English reading order.
        The table is a two dimensional 
        numpy array, going from north to south for each row.
        Within each column, it goes from west to east.
        Reading data sets self.zs
        """
        raise NotImplementedError()
        
    def free_data(self):
        """Free z elevation data read from file"""
        self._zs = None
        
    def _get_indices(self, x, y):
        """Helper method: return x and y indices for the given coords"""
        xindex = int((x - self._xtop)/self._xincrement)
        yindex = int((y - self._xtop)/self._yincrement)
        return xindex, yindex
        
    def get_z(self, x, y):
        """Return z at given x and y"""
        self.read_data()
        xindex, yindex = self._get_indices(x, y)
        return self._zs[xindex, yindex]
        
    def get_zslice(self, left, bottom, top, right):
        """
        Return a slice of the data array corresponding to the
        bounding box given of left, bottom, top, right
        Raises an index out of bounds error if the bounds are too large
        """
        self.read_data()
        xb, yb = self._get_indices(left, bottom)
        xt, yt = self._get_indices(top, right)
        return self._zs[xt:xb+1,yt:yb+1]
        
    def __str__(self):
        return '{0}: rows({1}), cols({2}), topx({3}), topy({4}), '  \
            'botx({5}), boty({6}), xincr({7}), yincr({8})'        \
            .format(os.path.basename(self._filename), self._rows, \
                self._cols, self._xtop, self._ytop, self._xbot,   \
                self._ybot, self._xincrement, self._yincrement)
                
def make_mesh_indices(nrows, ncols):
    """
    Given nrows and ncols, return the index array that draws a 
    mesh through the rectangular array
    """
    indices = []
        
    # return east/west lines
    i = 0
    for row in range(0, nrows):
    # for row in range(0, 1):
        indices.append(i)
        i += 1
        for col in range(1, ncols-1):
            indices.append(i)
            indices.append(i)
            i += 1
        indices.append(i)
        i += 1
        
    # return north/south lines
    for col in range(0, ncols):
    # for col in range(0, 1):
        i = col
        indices.append(i)
        i += self.ncols
        for row in range(1, nrows-1):
            indices.append(i)
            indices.append(i)
            i += ncols
        indices.append(i)
        i += ncols
  
    return indices
        
def make_triangle_indices(nrows, ncols):  
    """"
    Given nrows and ncols, return a clockwise triangle strip
    suitable for rendering by OpenGL
    """
    indices = []
        
    i = 0
    for row in range(0, nrows - 1):
        for col in range(0, ncols ):
            indices.append(i)
            indices.append(i+ncols)
            i += 1
            
    return indices



    

    

    
