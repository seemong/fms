from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import os
import numpy
import hgt
import math
import geofile
import hgt
import tif

def normalize(v):
    size = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    v[0] = v[0] / size
    v[1] = v[1] / size
    v[2] = v[2] / size
    return v
    
def _get_neighbors(mesh, row, col): 
    """
    Helper function. Given a rectangular numpy mesh z, return
    the two neighbors at the given row and column
    """
    n1_x = col
    if row < nrows - 1:
        n1_y = row + 1
    else:
        n1_y = row - 1
        
    n2_y = row
    if col <  ncols - 1:
        n2_x = col + 1
    else:
        n2_x = col - 1
        
    v1 = mesh[n1_x, n1_y]
    v2 = mesh[n2_x, n2_y]
    return v1, v2
    
def make_normals(mesh): 
    """
    Given a rectangular numpy mesh v, return the normals in a mesh of
    the same size
    """       
    nrows, ncols, naxis = mesh.shape
    normals = numy.zeros(nrows, ncols, naxis, dtype='float')
    
    # calculate normal vector for every point in the mesh
    for row in range(0, self.nrows):
        for col in range(0, ncols):
            coord = mesh[row, col]
            v1, v2 = _get_neighbors(mesh, row, col)
            norm = normalize(numpy.cross(v1 - coord, v2 - coord))
            if norm[2] >= 0:
                normals[row, col] = norm
            else:
                normals[row, col] = -1 * norm 
                
    return normals


class Terrain(object):
    """
    A terrain object presents an abstract interface to a set of
    terrain digital elevation files
    """
    
    def __init__(self):
        self._directories = []
        self._hgtFiles = []
        
    def add_data(self, filename):
        pass

if __name__ == '__main__':
    #h = hgt.HgtFile(sys.argv[1])
    #print(h.read_data())
    
    t = tif.TifFile(sys.argv[2])
    print(t)
    print(t.read_data())
    
    
