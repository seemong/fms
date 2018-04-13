from __future__ import print_function
import fileinput
import sys
import math
import os

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

    def vertices(self):
        self.file.seek(self.data_start, os.SEEK_SET)

        v = []
        for row in range(0, self.nrows):
            line = self.file.readline()
            split = line.split()
            assert len(split) == self.ncols
            for col in range(0, self.ncols):
                x = Esri._to_mercator(self.xllcorner + self.cellsize * col)
                y = Esri._to_mercator(self.yllcorner + (self.nrows - row - 1) * self.cellsize)
                z = float(split[col])/3
                v.append([x, y, z])
        return v

    def indices(self):
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

    def get_extent(self):
        return Esri._to_mercator(self.xllcorner), \
            Esri._to_mercator(self.yllcorner),     \
            Esri._to_mercator(self.xllcorner + self.cellsize * self.ncols),   \
            Esri._to_mercator(self.yllcorner + self.cellsize * self.nrows)



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
