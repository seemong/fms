from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
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

        self._g = gdal.Open(filename)
        self._cols = self._g.RasterXSize
        self._rows = self._g.RasterYSize
        count = self._g.RasterCount
        gt = self._g.GetGeoTransform()
        self._left = gt[0]
        self._xincrement = gt[1]
    
        self._top = gt[3]
        self._yincrement = -gt[5]
        
        self._right = self._left +  self._xincrement * (self._cols - 1)
        self._bottom = self._top - self._yincrement * (self._rows - 1)
               
    def read_data(self, row=0, col=0, numrows=None, numcols=None):
        """
        Read a slice from the geofile with row, col
        """
        return self._g.ReadAsArray(row, col, numrows, numcols)
        
    def get_left(self):
        """Return lat coordinates of western border"""
        return self._left
        
    def get_right(self):
        """Return lat coordinates of eastern border"""
        return self._right
        
    def get_top(self):
        """Return lon coordinates of northern"""
        return self._top
        
    def get_bottom(self):
        """Return lon coordinates of southern"""
        return self._bottom
        
    def get_extent(self):
        """Return left, bottom, right, top"""
        return self._left, self._bottom, \
            self._right, self._top
        
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
        
    def _xy_to_indices(self, x, y):
        """Helper method: return x and y indices for the given coords"""
        col = int((x - self._left)/self._xincrement)
        row = int((self._top - y)/self._yincrement)
        return col, row
        
    def _indices_to_xy(self, row, col):
        x = self._left + col * self._xincrement
        y = self._top - row * self._yincrement
        return x, y
        
    def get_data_slice(self, left, bottom, right, top):
        """
        Return a slice of the data array corresponding to the
        bounding box given of left, bottom, top, right
        Raises an index out of bounds error if the bounds are too large.
        This works in geo coordinates.
        """
        xb, yb = self._xy_to_indices(left, bottom)
        xt, yt = self._xy_to_indices(right, top)
        numx = xt - xb + 1
        numy = yb - yt + 1
        return self.read_data(xb, yt, numx, numy)
        
    def get_vertices(self, left, bottom, top, right):
        """
        Return the set of vertices in mercator coordinates
        as a 1D numpy array
        with the slice box coordinates given. Return also
        as second and third arguments the number of rows and cols.
        
        """
        data = self.get_data_slice(left, bottom, top, right)
        rows, cols = data.shape
        i = 0
        vertices = numpy.zeros((rows * cols, 3), dtype='float')
        for row in range(0, rows):
            for col in range(0, cols):
                x = _to_mercator(left + self._xincrement * col)
                y = _to_mercator(top - self._yincrement * row)
                vertices[i] = [x, y, data[row, col]]
                i += 1

        return vertices, rows, cols
        
    def __str__(self):
        return '{0}: rows({1}), cols({2}), left({3}), bottom({4}), '  \
            'top({5}),right({6}), xincr({7}), yincr({8})'        \
            .format(os.path.basename(self._filename), self._rows, \
                self._cols, self._left, self._bottom, self._top,   \
                self._right, self._xincrement, self._yincrement)
                
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
        i += ncols
        for row in range(1, nrows-1):
            indices.append(i)
            indices.append(i)
            i += ncols
        indices.append(i)
        i += ncols
  
    return indices
        
def make_triangle_indices(nrows, ncols):  
    """"
    Given nrows and ncols, return a counter clockwise triangle strip
    suitable for rendering by OpenGL. 
    """
    indices = []
        
    i = 0
    for row in range(0, nrows - 1):
        for col in range(0, ncols ):
            indices.append(i)
            indices.append(i+ncols)
            i += 1
            
    return indices
    
def flatten_rectangular_vertices(v):
    rows, cols, elts = v.shape
    return v.reshape((rows * cols, elts))
    
def _to_mercator(arc):
    """Take degrees of arc and multiply it to get a mercator number"""
    return arc * 11112


if __name__ == '__main__':
    import sys
    import pdb
    
    g = GeoFile(sys.argv[1])
    print(g)
    left, bottom, right, top = g.get_extent()
    print(left, bottom, right, top)
    d = g.get_data_slice(-122.45, 47.527, -122.192, 47.7167)
    print(d)
    
    pdb.set_trace()
    v = g.get_vertices(-122.45, 47.527, -122.192, 47.7167)
    print(v)
    rows, cols, _ = v.shape
    
    rows, cols, _ = v.shape
    mi = make_mesh_indices(rows, cols)
    # print(mi)
    ti = make_triangle_indices(rows, cols)
    # print(ti)
    

    
