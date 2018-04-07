from __future__ import print_function
from __future__ import nested_scopes
from builtins import *


class Coord(object):
    """
    A coordinate in the map has an id and x, y, z coords
    """
    def __init__(self, coords = (None, None, None)):
        self.coords = coords

    def __str__(self):
        return str(self.coords)

    def set_coords(self, x, y, z):
        """Set coordinates in 3d space"""
        self.coords = (x, y, z)
        
    def set_coords(self, coords):
        """Set coordinats in 3d space"""
        self.coords = coords

    def get_coords(self):
        """Get coords in 3d space"""
        return self.coords

    def get_x(self):
        """Return x coordinate -- longitude in the map"""
        return self.coords[0]
        
    def set_x(self, x):
        """Set x coordinate -- longitude in the map"""
        self.coords = (x, self.coords[1], self.coords[2])

    def get_y(self):
        """Return y coordinate -- latitude in the map"""
        return self.coords[1]
        
    def set_y(self, y):
        """Set y coordinate -- latitude in the map"""
        self.coords = (self.coords[0], y, self.coords[2])

    def get_z(self):
        """Return xz coordinate -- altitude in the map"""
        return self.coords[2]
        
    def set_z(self, z):
        """Set xz coordinate -- altitude in the map"""
        self.coords = (self.coords[0], self.coords[1], z)


if __name__ == '__main__':
    n = Coord((2, 3, 4))
    n.set_z(9)
    print(n)

