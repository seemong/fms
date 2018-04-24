from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import os
import numpy
import re
from osgeo import gdal
import math
import pdb

SECONDSPERDEGREE = 3600
ARCPERMETER = 0.000008992800576

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
        self._xsize = self._g.RasterXSize
        self._ysize = self._g.RasterYSize
        count = self._g.RasterCount
        gt = self._g.GetGeoTransform()
        self._left = gt[0]
        self._xincrement = gt[1]

        self._top = gt[3]
        self._yincrement = -gt[5]

        self._right = self._left +  self._xincrement * (self._xsize - 1)
        self._bottom = self._top - self._yincrement * (self._ysize - 1)

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

    def get_xsize(self):
        """How many cols there are in the data file"""
        return self._xsize

    def get_ysize(self):
        """How many rows there are in the data file"""
        return self._ysize

    def _lonlat_to_offset(self, lon, lat):
        """Helper method: return x and y indices for the given coords"""
        xoff = int((lon - self._left)/self._xincrement)
        yoff = int((self._top - lat)/self._yincrement)
        return xoff, yoff

    def _boundingbox_to_xyoffsize(self, left, bottom, right, top):
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
        return self.read_data(xoff, yoff, xsize, ysize), xoff, yoff, \
            xsize, ysize
        

    def get_vertices(self, left, bottom, right, top):
        """
        Return the set of vertices in as a 1D numpy array
        with the slice box coordinates given. Return also
        as second and third arguments the number of rows and cols.
        """
        xoff, yoff, xsize, ysize = \
            self._boundingbox_to_xyoffsize(left, bottom, right, top)
        return self.read_data_as_vertices(xoff, yoff, xsize, ysize), \
            xoff, yoff, xsize, ysize

    def get_tile(self, left, bottom, right, top):
        """
        Get a GeoTile based on the coordinates given
        """
        vertices, xoff, yoff, xsize, ysize = \
            self.get_vertices(left, bottom, right, top)
            
        left = self._left + xoff * self._xincrement
        bottom = self._top - (yoff + ysize - 1) * self._yincrement
        right = self._left + (xoff + xsize - 1) * self._xincrement
        top = self._top - yoff * self._yincrement
        
        return GeoTile(vertices, left, bottom, right, top, xsize, ysize)

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

def normalize(v):
    size = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    v[0] = v[0] / size
    v[1] = v[1] / size
    v[2] = v[2] / size
    return v

def get_neighbors(vertices, row, col, numrows, numcols):
    n1_x = col
    if row < numrows - 1:
        n1_y = row + 1
    else:
        n1_y = row - 1

    n2_y = row
    if col < numcols - 1:
        n2_x = col + 1
    else:
        n2_x = col - 1

    v1 = vertices[n1_x + n1_y * numcols]
    v2 = vertices[n2_x + n2_y * numcols]
    return v1, v2

def make_normals(vertices, numrows, numcols):
    """
    Return normal vectors based on neighbor averaging
    for a 1D vector array that represents a mesh containing
    the specified number of rows and cols
    """
    normals = []
    for row in range(0, numrows):
        for col in range(0, numcols):
            coord = numpy.array(vertices[col + row * numcols], 'f')
            v1, v2 = get_neighbors(vertices, row, col, numrows, numcols)
            norm = normalize(numpy.cross(v1 - coord, v2 - coord))
            if norm[2] >= 0:
                normals.append(norm)
            else:
                normals.append(-1 * norm)

    return normals
    
def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
    
def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], \
            a[0] * b[2] - a[2] * b[0], \
            a[0] * b[1] - a[1] * b[0]] 
            
def prod(s, v):
    return [s * v[0], s* v[1], s* v[2]]

def make_normals_fast(vertices, numrows, numcols):
    """
    Return normal vectors based on neighbor averaging
    for a 1D vector array that represents a mesh containing
    the specified number of rows and cols
    """
    normals = []
    for row in range(0, numrows):
        for col in range(0, numcols):
            coord = vertices[col + row * numcols]
            n1, n2 = get_neighbors(vertices, row, col, numrows, numcols)
            v1 = sub(n1, coord)
            v2 = sub(n2, coord)
            cp = cross(v1, v2)
            norm = normalize(cp)
            if norm[2] >= 0:
                normals.append(norm)
            else:
                normals.append(prod(-1, norm))

    return normals
    
class GeoTile(object):
    """
    GeoTile represents a list of vertices with an extent and a 
    geometry
    """
    def __init__(self, vertices, left, bottom, right, top, \
        xsize, ysize):
        self._vertices = vertices
        self._left = left
        self._bottom = bottom
        self._right = right
        self._top = top
        self._xsize = xsize
        self._ysize = ysize

    def get_vertices(self):
        return self._vertices

    def get_left(self):
        return self._left

    def get_bottom(self):
        return self._bottom

    def get_right(self):
        return self._right

    def get_top(self):
        return self._top

    def get_xsize(self):
        return self._xsize

    def get_ysize(self):
        return self._ysize

    def make_mesh_indices(self):
        return make_mesh_indices(self.get_ysize(), self.get_xsize())

    def make_triangle_indices(self):
        return make_triangle_indices(self.get_ysize(), self.get_xsize())

    def make_normals(self):
        # return make_normals(self.get_vertices(), self.get_rows(), self.get_cols())
        return make_normals_fast(self.get_vertices(), \
            self.get_ysize(), self.get_xsize())


if __name__ == '__main__':
    import sys
    import pdb

    g = GeoFile(sys.argv[1])
    print(g)
    left, bottom, right, top = g.get_extent()
    print(left, bottom, right, top)
    xinc = g.get_x_increment()
    yinc = g.get_y_increment()
    numrows = g.get_rows()
    numcols = g.get_cols()

    print('Reading vertices')
    vmin_lon, vmin_lat, vmax_lon, vmax_lat = (-121.921155, 46.779471, -121.517574, 46.979085)
    t = g.get_tile(vmin_lon, vmin_lat, vmax_lon, vmax_lat)
    cols = t.get_cols()
    n = t.make_normals()
    v = t.get_vertices()

    v0 = numpy.array(v[0])
    v1 = numpy.array(v[1])
    v2 = numpy.array(v[cols])
    print(n[0])
    
    print(normalize(numpy.cross(v1 - v0, v2 - v0)))

    # print(n)



    #i = make_mesh_indices(5, 3)
    # print(i)
