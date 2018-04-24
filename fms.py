from __future__ import print_function
from __future__ import nested_scopes
import pygame
from pygame.locals import *
import math
import sys
import numpy
import osm
import geofile
import mapobject
from display import Display
from plane import Plane
import pdb

def make_eye(r, theta, dispx, dispy):
    x = r * math.cos(theta) + dispx
    y = r * math.sin(theta) + dispy
    return x, y

def make_normals(count):
    normals = numpy.zeros((count, 3))
    for i in range(0, count):
        normals[i] = [0.0, 0.0, 1.0]
    return normals

def main():
    print('Hello World')
    
    vmin_lon, vmin_lat, vmax_lon, vmax_lat = \
        (-123.328, 47.0559, -121.0, 48.42)
    g = geofile.GeoFile('data/hgt15/15-A.tif')
 
    tile = g.get_tile(vmin_lon, vmin_lat, vmax_lon, vmax_lat)
    vertices = numpy.array(tile.get_vertices(), 'f')
    print('#vertices={0}'.format(len(vertices)))
    indices = numpy.array(tile.make_mesh_indices(), 'f')
    print('#indices={0}'.format(len(indices)))
    normals = numpy.array(tile.make_normals(), 'f')
    print('#normals={0}'.format(len(normals)))
    
    print('left={0},bottom={1},right={2},top={3}'.format( \
        tile.get_left(), tile.get_bottom(), \
        tile.get_right(), tile.get_top()))
    
    pdb.set_trace()
    
    plane = Plane()
    plane.set_position([-122.292221, 47.0599, geofile.meters_to_arc(1000)])
    plane.set_lookAt([-122.29221, 90, 0])
    plane.set_up([0, 0, 1])

    display = Display('test', width=800, height=800)
    display.create()
    display.set_perspective(90, 1, geofile.meters_to_arc(50), 10000)
    
    clock = pygame.time.Clock()
    while True:
        quit = False
        for event in display.get_events():
            if event.type == pygame.QUIT:
                quit = True
                break
        if quit:
            break

        display.predraw()
        
        eye = plane.get_position()
        lookAt = plane.get_lookAt()
        up = plane.get_up()
        display.lookAt(eye, lookAt, up)
        color = (1, 0, 0)
        display.draw_triangle_strip(vertices, indices, normals, color)
        
        display.postdraw()

        print(clock.tick())

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
