from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import os
import numpy
import re
from osgeo import gdal
import pdb

SECONDSPERDEGREE = 3600
ARCPERMETER = 1.0/1852/60

def meters_to_arc(meters):
    """Convert meters to arc units"""
    return meters * ARCPERMETER

class GeoFile(object):
    """
    Implements a an abstract Geo file representing either
    hgt, tif formats.
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

    def read_data(self, xoff=0, yoff=0, xsize=None, ysize=None):
        """
        Read a slice from the geofile with row, col
        """
        return self._g.ReadAsArray(xoff, yoff, xsize, ysize)

    def read_data_as_vertices(self, xoff=0, yoff=0, \
        xsize=None, ysize=None):
        """
        Read a slice from the geofile and return as a 1D numpy
        array with the elevation data in units of arc
        """
        data = self.read_data(xoff, yoff, xsize, ysize)
        rows, cols = data.shape
        vertices = []
        startx = self._left + xoff * self._xincrement
        starty = self._top - yoff * self._yincrement
        for row in range(0, rows):
            for col in range(0, cols):
                x = (startx + self._xincrement * col)
                y = (starty - self._yincrement * row)
                elevation_in_arc = meters_to_arc(data[row, col])
                vertices.append([x, y, elevation_in_arc])
                # vertices.append([x, y, data[row, col]])
        return vertices

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
        return self._cols

    def get_rows(self):
        """How many rows there are in the data file"""
        return self._rows

    def _lonlat_to_offset(self, lon, lat):
        """Helper method: return x and y indices for the given coords"""
        xoff = int((lon - self._left)/self._xincrement)
        yoff = int((self._top - lat)/self._yincrement)
        return xoff, yoff

    def _boundingbox_to_xyoffsize(self, left, bottom, top, right):
        """
        Given coordinates left, bottom, top, right, convert this to
        xoffset, yoffset, xsize and ysize to use to read data
        """
        xb, yb = self._lonlat_to_offset(left, bottom)
        xt, yt = self._lonlat_to_offset(right, top)
        xsize = xt - xb + 1
        ysize = yb - yt + 1
        return xb, yt, xsize, ysize

    def get_data_slice(self, left, bottom, right, top):
        """
        Return a slice of the data array corresponding to the
        bounding box given of left, bottom, top, right in lat/lon.
        Raises an index out of bounds error if the bounds are too large.
        This works in geo coordinates.
        """
        xoff, yoff, xsize, ysize = \
            self._boundingbox_to_xyoffsize(left, bottom, right, top)
        return self.read_data(xb, yt, xsize, ysize)

    def get_vertices(self, left, bottom, top, right):
        """
        Return the set of vertices in as a 1D numpy array
        with the slice box coordinates given. Return also
        as second and third arguments the number of rows and cols.
        """
        xoff, yoff, xsize, ysize = \
            self._boundingbox_to_xyoffsize(left, bottom, right, top)
        return self.read_data_as_vertices(xoff, yoff, xsize, ysize), \
            ysize, xsize

    def __str__(self):
        return '{0}: rows({1}), cols({2}), left({3}), bottom({4}), '  \
            'top({5}),right({6}), xincr({7}), yincr({8})'             \
            .format(os.path.basename(self._filename), self._rows,     \
                self._cols, self._left, self._bottom, self._top,      \
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
    xinc = g.get_x_increment()
    yinc = g.get_y_increment()

    d = g.read_data()
    print(d.max())



    #i = make_mesh_indices(5, 3)
    # print(i)
