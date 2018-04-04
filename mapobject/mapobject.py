from __future__ import print_function
from __future__ import nested_scopes
from builtins import *

class Mapobject(object):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

# Node in the map
class Node(Mapobject):
    """
    A node in the map has an id coordinates, a type and attributes
    """
    def __init__(self, id, coords = (None, None, None)):
        super().__init__(id)
        self.coords = coords
        self.attribs = {}

    def __str__(self):
        return str(self.get_id()) + ':' + str(self.get_coords()) + ':' + \
            str(self.get_attribs())

    def set_coords(self, x, y, z):
        """Set coordinates in 3d space"""
        self.coords = (x, y, z)

    def set_coords(self, coords):
        self.coords = coords

    def get_coords(self):
        """Get coords in 3d space"""
        return self.coords

    def get_x(self):
        """Return x coordinate -- longitude in the map"""
        return self.coords[0]

    def get_y(self):
        """Return y coordinate -- latitude in the map"""
        return self.coords[1]

    def get_z(self):
        """Return xz coordinate -- altitude in the map"""
        return self.coords[2]

    def get_longitude(self):
        """Return longitude in the map"""
        return self.get_x()

    def get_latitude(self):
        """Return longitude in the map"""
        return self.get_y()

    def get_altitude(self):
        """Return altitude in the map"""
        return self.get_z()

    def add_attrib(self, key, value):
        """Add an attribute, which is a key, value pair"""
        self.attribs[key] = value

    def get_attrib(self, key):
        """Return the value of a key attribute"""
        return self.attribs[key]

    def get_attribs(self):
        """Return dictionary of all key, value attributes"""
        return self.attribs

class Way(Mapobject):
    def __init__(self, id):
        super().__init__(id)
        self.nodes = []

    def __str__(self):
        s = str(self.get_id()) + ':'
        for n in self.nodes:
            s += (str(n) + ';')
        return s

    def get_nodes(self):
        """Return the list of nodes belonging to this way"""
        return self.nodes

    def num_nodes(self):
        return len(self.nodes)

    def add_node(self, node):
        self.nodes.append(node)

    def __str__(self):
        s = str(self.get_id()) + ':'
        for n in self.nodes:
            s += (str(n) + ';')
        return s

if __name__ == '__main__':
    n1 = Node('chester', (2, 3, 4))
    n2 = Node('foo')
    n2.set_coords((10, 11, 12))
    n2.add_attrib("k", "v")

    w = Way("test-way")
    w.add_node(n1)
    w.add_node(n2)

    print(w)
