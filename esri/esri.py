from __future__ import print_function
import fileinput
import sys
import math
import numpy
import os

def normalize(v):
    size = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    v[0] = v[0] / size
    v[1] = v[1] / size
    v[2] = v[2] / size
    return v

class Esri(object):
    """Represents an ESRI ASCII file"""

    @classmethod
    def _read_esri_header(cls, line, key):
        split = line.split()
        assert split[0] == key
        return split[1]

    def __init__(self, filename):
        self.file = open(filename, 'r')

        line = self.file.readline()
        self.ncols = int(Esri._read_esri_header(line, 'ncols'))

        line = self.file.readline()
        self.nrows = int(Esri._read_esri_header(line, 'nrows'))

        line = self.file.readline()
        self.xllcorner = float(Esri._read_esri_header(line, 'xllcorner'))

        line = self.file.readline()
        self.yllcorner =  float(Esri._read_esri_header(line, 'yllcorner'))

        line = self.file.readline()
        self.cellsize = float(Esri._read_esri_header(line, 'cellsize'))

        line = self.file.readline()
        self.NODATA_value = float(Esri._read_esri_header(line, 'NODATA_value'))
        
        self.vertices = None

        self.data_start = self.file.tell()

    def __str__(self):
        return 'ncols=' + str(self.ncols) + ', nrows=' + str(self.nrows)

    def xurcorner(self):
        """x upper right corner"""
        return self.xllcorner + (self.ncols - 1) * self.cellsize

    def yurcorner(self):
        """y upper right corner"""
        return self.yllcorner + (self.nrows - 1) * self.cellsize

    def get_row_index(self, y):
        idx = self.nrows - int((y - self.yllcorner) / self.cellsize)
        return idx, self.yllcorner + (self.nrows - idx - 1) * self.cellsize

    def get_col_index(self, x):
        idx = int((x - self.xllcorner) / self.cellsize)
        return idx, self.xllcorner + self.cellsize * idx

    def filter(self, left, bottom, right, top):
        startrow, starty = self.get_row_index(top)
        endrow, endy = self.get_row_index(bottom)
        startcol, startx = self.get_col_index(left)
        endcol, endx = self.get_col_index(right)

        print('ncols         ' + str(endcol - startcol + 1))
        print('nrows         ' + str(endrow - startrow + 1))
        print('xllcorner     ' + str(endx))
        print('yllcorner     ' + str(endy))
        print('cellsize      ' + str(self.cellsize))
        print('NODATA_value  ' + '-9999')

        # start at beginning of data
        self.file.seek(self.data_start, os.SEEK_SET)

        # skip to the correct row
        for i in range(0, startrow):
            self.file.readline()             # throw data away

        # read data from the correct rows
        for row in range(startrow, endrow+1):
            line = self.file.readline()

            split = line.split()
            for col in range(startcol, endcol + 1):
                print(split[col], end=' ')
            print("")

    @classmethod
    def _to_mercator(cls, arc):
        """Take degrees of arc and multiply it to get a mercator number"""
        return arc * 11112

    def get_vertices(self):
        if not self.vertices == None:
            return self.vertices
            
        self.file.seek(self.data_start, os.SEEK_SET)

        self.vertices = []
        for row in range(0, self.nrows):
            line = self.file.readline()
            split = line.split()
            assert len(split) == self.ncols
            for col in range(0, self.ncols):
                x = Esri._to_mercator(self.xllcorner + self.cellsize * col)
                y = Esri._to_mercator(self.yllcorner + (self.nrows - row - 1) * self.cellsize)
                z = float(split[col])/3
                self.vertices.append([x, y, z])
                
        return self.vertices

    def get_mesh_indices(self):
        indices = []
        
        # return east/west lines
        i = 0
        for row in range(0, self.nrows):
        # for row in range(0, 1):
            indices.append(i)
            i += 1
            for col in range(1, self.ncols-1):
                indices.append(i)
                indices.append(i)
                i += 1
            indices.append(i)
            i += 1
            
        # return north/south lines
        for col in range(0, self.ncols):
        # for col in range(0, 1):
            i = col
            indices.append(i)
            i += self.ncols
            for row in range(1, self.nrows-1):
                indices.append(i)
                indices.append(i)
                i += self.ncols
            indices.append(i)
            i += self.ncols
  
        return indices
        
    def get_triangle_indices(self):
        indices = []
        
        i = 0
        for row in range(0, self.nrows - 1):
            for col in range(0, self.ncols ):
                indices.append(i)
                indices.append(i+self.ncols)
                i += 1
            
        return indices
            

    def get_extent(self):
        return Esri._to_mercator(self.xllcorner), \
            Esri._to_mercator(self.yllcorner),     \
            Esri._to_mercator(self.xllcorner + self.cellsize * self.ncols),   \
            Esri._to_mercator(self.yllcorner + self.cellsize * self.nrows)

    def get_neighbors(self, row, col):
        n1_x = col
        if row < self.nrows - 1:
            n1_y = row + 1
        else:
            n1_y = row - 1
            
        n2_y = row
        if col < self.ncols - 1:
            n2_x = col + 1
        else:
            n2_x = col - 1
            
        vertices = self.get_vertices()
        v1 = vertices[n1_x + n1_y * self.ncols]
        v2 = vertices[n2_x + n2_y * self.ncols]
        return v1, v2
    


    def get_normals(self):
        vertices = self.get_vertices()
        normals = numpy.zeros((self.nrows * self.ncols, 3), dtype='float')
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                coord = numpy.array(vertices[col + row * self.ncols], 'f')
                v1, v2 = self.get_neighbors(row, col)
                norm = normalize(numpy.cross(v1 - coord, v2 - coord))
                if norm[2] >= 0:
                    normals[col + row * self.ncols] = norm
                else:
                    normals[col + row * self.ncols] = -1 * norm 
          
        return normals


if __name__ == '__main__':
    esri = Esri(sys.argv[1])
    # esri.filter(-121.90, 46.75, -121.56, 46.96)
    v = esri.vertices()
    i = esri.indices()
    # print(v)
    print(esri.nrows, esri.ncols)
    print(len(v))
    print(i)
    print(len(i))
