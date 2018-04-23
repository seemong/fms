from __future__ import print_function
from __future__ import nested_scopes
from builtins import *
import sys
import xml.etree.ElementTree as etree
import time
import argparse
from mapobject import *
import math
import numpy as np

def _to_mercator(arc):
    """Take degrees of arc and multiply it to get a mercator number"""
    return arc * 11112

def _make_osm_node(elem):
    """
    Make a Node out of the OSM XML element
    """
    assert elem.tag == 'node'
    id = elem.get('id')
    lat = _to_mercator(float(elem.get('lat')))
    lon = _to_mercator(float(elem.get('lon')))

    return Node(id, (lon, lat, 0))

def _get_node_distance(m, id1, id2):
    coord1 = m.get_node_from_id(id1).get_coords()
    coord2 = m.get_node_from_id(id2).get_coords()
    dist = math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)
    return dist

def _make_osm_way(elem, m, min_node_separation=0):
    """
    Make a Way out of the OSM XML tree.
    Filter nodes so that the min separation between nodes is satisfied
    Update all nodes to have the altitude if it's an elevation
    contour
    """
    id = elem.get('id')
    w = Way(id)

    # get all nodes belonging to the way
    old_id = None
    first_id = None
    for nd in elem.findall('nd'):
        node_id = nd.get('ref')
        if first_id == None:
            first_id = node_id

        # filter node to have a min separation
        if old_id != None:
            dist = _get_node_distance(m, old_id, node_id)
            if dist < min_node_separation and node_id != first_id:
                continue

        w.add_node_id(node_id)
        old_id = node_id

    # find all the associated attributes
    for tag in elem.findall('tag'):
        k = tag.get('k')
        v = tag.get('v')
        w.add_attrib(k, v)

    # check for elevation contours
    try:
        ele = float(w.get_attrib('ele'))
    except:
        print('No elevation')
        return w

    # set elevation and convert feet to meters
    for id in w.get_node_ids():
        node = m.get_node_from_id(id)
        node.set_altitude(ele/3)

    return w

def make_osm_map(name, osmf, min_node_separation=0, min_ele_separation=0):
    """
    Given the OSM file osmf, read the file and make a Map out of it.
    Implement XML reading in a memory efficient manner.
    Return the map that was made
    """

    xml = open(osmf, "r")
    context = etree.iterparse(xml, events=("start", "end"))
    # turn into an iterable
    context = iter(context)
    # get the root
    event, root = context.next()

    # The map we will return
    m = Map(name)

    # save flag determines whether or not to save the XML tree
    # in memory. If it's not set, the tree and elements are freed
    # at each iteration, in order to save on memory
    save = False
    for event, elem in context:
        if event == 'start' and \
            (elem.tag == 'way' or elem.tag == 'node'):
            # save tree elements until we see the end
            save = True
        elif event == 'end' and elem.tag == 'node':
            node = _make_osm_node(elem)
            m.add_node(node)
            save = False
        elif event == 'end' and elem.tag == 'way':
            # tree = etree.ElementTree(elem)
            way = _make_osm_way(elem, m, min_node_separation)
            ele = way.get_elevation()
            if ele % min_ele_separation != 0:
                print('Skipping ele', ele)
                continue

            m.add_way(way)
            print('Ele', ele)
            save = False

        if not save:
            elem.clear()
            root.clear()

    # clear the tree at the end
    root.clear()

    return m

if __name__ == "__main__":
    assert len(sys.argv) == 2
    m = make_osm_map("The Map", sys.argv[1])
    ways = m.get_all_ways()
    w = ways[0]
    for id in w.get_node_ids():
        n = m.get_node_from_id(id)
        print(n)
