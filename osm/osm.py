from __future__ import print_function
import sys
import xml.etree.ElementTree as etree

def main():
    print('Hello OSM')
    
    spinner = ['/', '-', '\\', '|']
    count = 0;

    xml = open("washington-latest.osm", "r")
    for event, elem in etree.iterparse(xml):
        if elem.tag == 'way':
            print(elem.tag, elem.attrib)


if __name__ == "__main__":
    main()
