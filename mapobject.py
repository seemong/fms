from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
from geometry import Coord
import numpy as np
from collections import OrderedDict

# Map objects have an id and each has a list of attributes
class Mapobject(object):
    def __init__(self, id):
        """Every map object has an id"""
        self.__id = id
        self.__attribs = dict()

    def __str__(self):
        return 'Mapobject(' + self.get_id() + ')' + \
            str(self.get_attribs())

    def get_id(self):
        """Return id of the map object"""
        return self.__id

    def add_attrib(self, key, value):
        """Add an attribute, which is a key, value pair"""
        self.__attribs[key] = value

    def set_attribs(self, attribs):
        self.__attribs = attribs

    def get_attrib(self, key):
        """Return the value of a key attribute"""
        return self.__attribs[key]

    def get_attribs(self):
        """Return dictionary of all key, value attributes"""
        return self.__attribs

# Node in the map
class Node(Mapobject, Coord):
    """
    A node in the map has an id and coordinates.
    It adds lat/long/alt methods to set coordinates
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
    A way is a set of node ids and associated attributes.
    """
    def __init__(self, id):
        super().__init__(id)
        self.__node_ids = []

    def __str__(self):
        return "Way(" + self.get_id() + '):' + \
            'attribs:(' + str(self.get_attribs()) + '):node_ids(' + \
            str(self.get_node_ids()) + ')'

    def get_node_ids(self):
        """Return the list of node ids belonging to this way"""
        return self.__node_ids

    def num_nodes(self):
        return len(self.__node_ids)

    def add_node_id(self, node_id):
        """
        Add this node with the given id to the way
        """
        self.__node_ids.append(node_id)

    def get_elevation(self):
        """Return elevation if there is one"""
        return float(self.get_attrib('ele'))


class Map(Mapobject):
    """
    A map is a collection of nodes and ways
    """
    def __init__(self, id):
        super().__init__(id)

        # keep the nodes as a dictionary that indexes
        # to a tuple (index, Node) based on node id
        self.__nodes_dict = OrderedDict()

        # keep a way as a dictionary that indexes to a tuple
        # (index, Way) based on way id
        self.__ways_dict = OrderedDict()

        # last node index is incremented each time a node is added
        # and similarly for the last node index
        self.__last_node_index = self.__last_way_index = 0

        # initialize the extents of the map
        self.__max_lon = float('-inf')
        self.__min_lon = float('inf')
        self.__max_lat = float('-inf')
        self.__min_lat = float('inf')

        # store node indices for faster access
        self.__node_segments_for_way = dict()

    def __str__(self):
        return 'Map(' + self.get_id() + '):\nNodes(' + \
            str(self.get_all_node_ids()) + \
            ')\nWays(' + str(self.get_all_way_ids()) + ')'

    def add_node(self, node):
        """Add node to map"""
        self.__nodes_dict[node.get_id()] = \
            (self.__last_node_index, node)
        self.__last_node_index += 1

    def get_all_nodes(self):
        """Get list of nodes in this map"""
        return [ v[1] for v in self.__nodes_dict.values() ]

    def get_node_from_id(self, id):
        """Return the node given the id"""
        return self.__nodes_dict[id][1]

    def get_all_node_ids(self):
        """Return all the node ids in order"""
        return self.__nodes_dict.keys()

    def get_all_node_coords(self):
        """Get a list of all node coords"""
        return [v[1].get_coords() for v in self.__nodes_dict.values()]

    def get_node_index_from_id(self, node_id):
        """Return index of node in the numpy node array"""
        return self.__nodes_dict[node_id][0]

    def add_way(self, way):
        """
        Add way to this map.
        Also adds all nodes to the map if they aren't already in the map
        """
        self.__ways_dict[way.get_id()] = (self.__last_way_index, way)
        self.__last_way_index += 1

        # figure out the extends
        for node_id in way.get_node_ids():
            node = self.get_node_from_id(node_id)
            lat = node.get_latitude()
            lon = node.get_longitude()
            self.__min_lat = min(self.__min_lat, lat)
            self.__max_lat = max(self.__max_lat, lat)
            self.__min_lon = min(self.__min_lon, lon)
            self.__max_lon = max(self.__max_lon, lon)

    def get_extent(self):
        """
        Return the extent of the map
        min_lon, min_lat, max_long, max_lat
        """
        return self.__min_lon, self.__min_lat, \
            self.__max_lon, self.__max_lat

    def get_all_ways(self):
        """Get list of ways to this map"""
        return [ v[1] for v in self.__ways_dict.values() ]

    def get_way_from_id(self, id):
        """Return the way given the way id"""
        return self.__ways_dict[id][1]

    def get_all_way_ids(self):
        """Return all the way ids in order"""
        return self.__ways_dict.keys()

    def get_node_indices_for_way(self, way):
        """Given a way, find the indices for each of the nodes"""
        return [self.get_node_index_from_id(id) \
            for id in way.get_node_ids()]

    @classmethod
    def _connect_indices(cls, indices):
        result = [indices[0]]
        for i in range(1, len(indices) - 1):
            result.append(indices[i])
            result.append(indices[i])
        result.append(indices[len(indices) - 1])
        return result

    def get_node_segment_indices_for_way(self, way):
        try:
            indices = self.__node_segments_for_way[way.get_id()]
        except:
            indices = Map._connect_indices(self.get_node_indices_for_way(way))
            self.__node_segments_for_way[way.get_id()] = indices
        return indices

    def get_all_node_coords_numpy(self):
        """
        Return the coordinates for all nodes stored in
        numpy format
        """
        return np.array(self.get_all_node_coords(), dtype='float')


if __name__ == '__main__':
    n1 = Node('chester', (2, 3, 4))
    n2 = Node('foo')
    n2.set_coords((10, 11, 12))
    n2.add_attrib("k", "v")

    w = Way("test-way")
    w.add_node_id(n1.get_id())
    w.add_node_id(n2.get_id())
    w.add_attrib('ele', 400)

    m = Map("themap")
    m.add_node(n1)
    m.add_node(n2)
    m.add_way(w)

    print(m)
    for n in m.get_all_nodes():
        print(n)
    for w in m.get_all_ways():
        print(w)
    print(m.get_all_node_coords())
    print(m.get_node_indices_for_way(w))
    print(m.get_all_node_coords_numpy())
    min_lon, min_lat, max_lon, max_lat = m.get_extent()
    print(min_lon, min_lat, max_lon, max_lat)
