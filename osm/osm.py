from __future__ import print_function
import sys
import xml.etree.ElementTree as etree
import time

def main():
    print('Hello OSM')
    count = 0
    
    xml = open("washington-latest.osm", "r")
    for event, elem in etree.iterparse(xml):
        count += 1

        if elem.tag == 'way':
            print(elem.tag, elem.attrib)

    print('Parsed {0} elements'.format(count))



if __name__ == "__main__":
    main()
