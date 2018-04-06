from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
from geometry import Coord
import pdb

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

# Map objects have an id and each has a list of attributes
class Mapobject(object):
    def __init__(self, id):
        """Every map object has an id"""
        self.id = id
        self.attribs = dict()
        
    def __str__(self):
        return 'Mapobject(' + self.get_id() + ')' + \
            str(self.attribs)
        
    def get_id(self):
        """Return id of the map object"""
        return self.id
        
    def add_attrib(self, key, value):
        """Add an attribute, which is a key, value pair"""
        self.attribs[key] = value
        
    def set_attribs(self, attribs):
        self.attribs = attribs

    def get_attrib(self, key):
        """Return the value of a key attribute"""
        return self.attribs[key]

    def get_attribs(self):
        """Return dictionary of all key, value attributes"""
        return self.attribs

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
            str(self.get_coords()) + ':attribs(' + \
            str(self.get_attribs()) + ')'

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
    """
    A way is a set of nodes and associated attributes.
    Implemented as a dictionary of nodes referenced by the node id.
    """
    def __init__(self, id):
        super().__init__(id)
        self.nodes = []
        self.max_lat = None
        self.min_lat = None
        self.max_lon = None
        self.min_lon = None
        self.attribs = dict()

    def __str__(self):
        return "Way(" + self.get_id() + '):' + \
            'attribs:(' + str(self.get_attribs()) + '):' + \
            _listify(self.get_nodes()) + ')'

    def get_nodes(self):
        """Return the list of nodes belonging to this way"""
        return self.nodes

    def num_nodes(self):
        return len(self.nodes)

    def add_node(self, node):
        """
        Add this node to the way, and calculate the min/max 
        bounding box for the way
        """
        node_id = node.get_id()
        self.nodes.append(node)
        
        # set max/min bounds
        lat = node.get_latitude()
        lon = node.get_longitude()
        if self.max_lat == None:
            self.min_lat = self.max_lat = lat
            self.min_lon = self.max_lon = lon
            return
        if self.min_lat > lat:
            self.min_lat = lat
        if self.max_lat < lat:
            self.max_lat = lat
        if self.min_lon > lon:
            self.min_lon = lon
        if self.max_lon < lon:
            self.max_lon = lon
        
    def get_bounds(self):
        """Return the bounds (min lat, min long, max lat, max long)"""
        return (self.min_lat, self, min_long, 
            self.max_lat, self.max_long)

        
        
# A Map is a collection of nodes and ways
class Map(Mapobject):
    def __init__(self, id):
        super().__init__(id)
        self.nodes = dict()
        self.ways = dict()
        
    def __str__(self):
        node_list = self.get_nodes()
        node_list_str = _listify(node_list)
        ways_list = self.get_ways()
        ways_list_str = _listify(ways_list)
    
        return 'Map(' + self.get_id() + '):\nNodes(' + \
            _listify(self.get_nodes()) \
            + ')\nWays(' + _listify(self.get_ways()) \
            + ')'
        
    def add_node(self, node):
        """Add node to map"""
        self.nodes[node.get_id()] = node
        
    def get_nodes(self):
        """Get list of nodes in this map"""
        return [ v for v in self.nodes.values() ]
        
    def make_node_finder(self):
        """
        Return a function that finds a node in this map
        """
        n = self.nodes
        def dictionary_finder(id):
            return n[id]
        return dictionary_finder
        
    def add_way(self, way):
        """
        Add way to this map. 
        Also adds all nodes to the map if they aren't already in the map
        """
        for node in way.get_nodes():
            if not node in self.nodes:
                self.add_node(node)
        self.ways[way.get_id()] = way
        
    def get_ways(self):
        """Get list of ways to this map"""
        return [ v for v in self.ways.values() ]
        

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

