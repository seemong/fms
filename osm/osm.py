from __future__ import print_function
import sys
import xml.etree.ElementTree as etree
import time
import argparse
from geometry.mapobject import *

def make_osm_node(elem):
    """
    Make a Node out of the OSM XML element
    """
    assert elem.tag == 'node'
    id = elem.get('id')
    lat = float(elem.get('lat'))
    lon = float(elem.get('lon'))
    
    return Node(id, (lon, lat, 0))
    
def make_osm_way(elem):
    """
    Make a Way out of the OSM XML tree. 
    Update all nodes to have the altitude if it's an elevation 
    contour
    """
    id = elem.get('id')
    w = Way(id)
    
    # get all nodes belonging to the way
    for nd in elem.findall('nd'):
        node_id = nd.get('ref')
        w.add_node_id(node_id)
        
    # find all the associated attributes
    for tag in elem.findall('tag'):
        k = tag.get('k')
        v = tag.get('v')
        w.add_attrib(k, v)
        
    # check for elevation contours
    try:
        ele = float(w.get_attrib('ele'))
        for n in w.get_nodes():
            n.set_altitude(ele)
    except:
        pass
        
    return w

def make_osm_map(osmf):
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

    # The map we will return, together with a function that
    # will return the node in the map given an id
    m = Map('The Map')
    
    save = False
    for event, elem in context:
        if event == 'start' and \
            (elem.tag == 'way' or elem.tag == 'node'):
            # save tree elements until we see the end
            save = True
        elif event == 'end' and elem.tag == 'node':
            node = make_osm_node(elem)
            m.add_node(node)
            save = False
        elif event == 'end' and elem.tag == 'way':
            # tree = etree.ElementTree(elem)
            way = make_osm_way(elem)
            m.add_way(way)
            save = False

        if not save:
            elem.clear()
            root.clear()
    
    # clear the tree at the end
    root.clear()

    return m

if __name__ == "__main__":
    m = make_osm_map(sys.argv[1])
    ways = m.get_ways()
    print(m.get_node_indices_for_way(ways[2]))
