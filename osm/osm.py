from __future__ import print_function
import sys
import xml.etree.ElementTree as etree
import time
import argparse
from map import *

def main():
    sys.stderr.write('Hello OSM\n')

    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', action='append')
    tag_args = parser.parse_args(sys.argv[1:]).tag
    tags = []
    for arg in tag_args:
        kv = arg.split(':')
        tags.append({ 'k' : kv[0], 'v' : kv[1] })

    count = 0
    ways = 0

    xml = open("washington-latest.osm", "r")
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
        elif event == "end" and elem.tag == 'way':
            # write the way out if it's what we wanted
            tree = etree.ElementTree(elem)
            for tag in tree.findall('tag'):
                k = tag.get('k')
                v = tag.get('v')
                found = False
                for wanted in tags:
                    if k == wanted['k'] and v == wanted['v']:
                        tree.write(sys.stdout)
                        sys.stdout.write('\n')
                        ways += 1
                        found = True
                        break
                if found:
                    break
            save = False

        if not save:
            elem.clear()
            root.clear()

        if count % 10000 == 0:
            sys.stderr.write('{0}\n'.format(count))

    sys.stderr.write('Parsed {0} elements\n'.format(count))
    sys.stderr.write('Dumped {0} ways\n'.format(ways))



if __name__ == "__main__":
    main()
