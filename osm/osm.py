from __future__ import print_function
import sys
import xml.etree.ElementTree as etree
import time
import argparse
from mapobject.mapobject import *

def make_osm_node(elem):
    assert elem.tag == 'node'
    id = elem.get('id')
    lat = elem.get('lat')
    lon = elem.get('lom')
    return Node(id, (lon, lat, 0))

def main():
    count = 0
    nodes = 0
    ways = 0
    map = Map('The Map')
    
    f = sys.argv[0]

    xml = open(f, "r")
    context = etree.iterparse(xml, events=("start", "end"))

    # turn into an iterable
    context = iter(context)

    # get the root
    event, root = context.next()

    save = False
    for event, elem in context:
        count += 1

        if event == 'start' and elem.tag == 'way':
            save = True
        elif event == "end" and elem.tag == 'node':
            node = make_osm_node(elem)
            m.add_node(node)
        elif event == 'end' and elem.tag == 'way':
            tree = etree.ElementTree(elem)

            # write the way out if it's what we wanted
            # for tag in tree.findall('tag'):
            #    k = tag.get('k')
            #    v = tag.get('v')
            #    found = False
            #    for wanted in tags:
            #        if k == wanted['k'] and v == wanted['v']:
            #            tree.write(sys.stdout)
            #            sys.stdout.write('\n')
            #            ways += 1
            #            found = True
            #            break
            #    if found:
            #        break
            save = False

        if not save:
            elem.clear()
            root.clear()


    print(m)
    print('Parsed {0} elements\n'.format(count))
    print('Dumped {0} ways\n'.format(nodes))
    print('Dumped {0} ways\n'.format(ways))



if __name__ == "__main__":
    main()
