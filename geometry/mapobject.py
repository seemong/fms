from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
from geometry import Coord

# Map objects have an id and each has a list of attributes
class Mapobject(object):
    def __init__(self, id):
        """Every map object has an id"""
        self.id = id
        self.attribs = {}

    def get_id(self):
        """Return id of the map object"""
        return self.id
        
    def add_attrib(self, key, value):
        """Add an attribute, which is a key, value pair"""
        self.attribs[key] = value

    def get_attrib(self, key):
        """Return the value of a key attribute"""
        return self.attribs[key]

    def get_attribs(self):
        """Return dictionary of all key, value attributes"""
        return self.attribs
        
def _listify(l):
    """
    Helper function -- convert list l to a string
    """
    s = ''
    for i in range(0, len(l)):
        e = l[i]
        s = s + str(e)
        if i < len(l) - 1:
            s = s + ';'
    return s

# Node in the map
class Node(Mapobject, Coord):
    """
    A node in the map has an id and coordinates
    """
    def __init__(self, id = None, coords = (None, None, None)):
        Mapobject.__init__(self, id)
        Coord.__init__(self, coords)

    def __str__(self):
        return 'Node(' + str(self.get_id()) + '):' + \
            str(self.get_coords()) + ':' + \
            str(self.get_attribs())

    def get_longitude(self):
        """Return longitude in the map"""
        return self.get_x()
        
    def set_longitude(self, longitude):
        """Set longitude in the map"""
        self.set_y(longitude)

    def get_latitude(self):
        """Return latitude in the map"""
        return self.get_y()
        
    def set_latitude(self, latitude):
        """Set latitude in the map"""
        self.get_x(latitude)

    def get_altitude(self):
        """Return altitude in the map"""
        return self.get_z()
        
    def set_altitude(self, altitude):
        """Set altitude in the map"""
        self.set_z(altitude)


class Way(Mapobject):
    def __init__(self, id):
        super().__init__(id)
        self.nodes = []

    def __str__(self):
        return "Way(" + str(self.get_id()) + '):' + \
            _listify(self.nodes, 'Node')
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
        
# A Map is a collection of nodes and ways
class Map(Mapobject):
    def __init__(self, id):
        super().__init__(id)
        self.nodes = []
        self.ways = []
        
    def __str__(self):
        return 'Map(' + self.get_id() + '):Nodes(' + \
            _listify(self.nodes) \
            + '):Ways(' + _listify(self.ways) \
            + ')'
        
    def add_node(self, node):
        """Add node to map"""
        self.nodes.append(node)
        
    def get_nodes(self):
        """Get list of nodes in this map"""
        return self.nodes
        
    def add_way(self, way):
        """
        Add way to this map. 
        Also adds all nodes to the map if they aren't already in the map
        """
        for n in way.get_nodes():
            if not n in self.nodes:
                self.nodes.append(n)
        self.ways.append(way)
        
    def get_ways(self):
        """Get list of ways to this map"""
        return self.ways
        

if __name__ == '__main__':
    n1 = Node('chester', (2, 3, 4))
    n2 = Node('foo')
    n2.set_coords((10, 11, 12))
    n2.add_attrib("k", "v")

    w = Way("test-way")
    w.add_node(n1)
    w.add_node(n2)
    
    m = Map("themap")
    #m.add_node(n1)
    m.add_node(n2)
    m.add_way(w)

    print(m)

