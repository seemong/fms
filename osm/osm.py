from __future__ import print_function
import sys
import xml.etree.ElementTree as etree
import time

def main():
    sys.stderr.write('Hello OSM\n')
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
            tree = etree.ElementTree(elem)
            tree.write(sys.stdout)
            sys.stdout.write('\n')
            save = False
            ways += 1

        if not save:
            elem.clear()
            root.clear()

        if count % 10000 == 0:
            sys.stderr.write('{0}\n'.format(count))

    sys.stderr.write('Parsed {0} elements\n'.format(count))
    sys.stderr.write('Dumped {0} ways\n'.format(ways))



if __name__ == "__main__":
    main()
