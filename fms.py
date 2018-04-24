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
    
    # set initial position
    vmin_lon, vmin_lat, vmax_lon, vmax_lat = \
     (-122.419808, 47.558547, -122.179825, 47.71655)
    eye = ((vmin_lon + vmax_lon) / 2, vmin_lat, geofile.meters_to_arc(2000))
    lookAt = (eye[0], 90, 0)
    up = (0, 0, 1)
    center = ((vmin_lon + vmax_lon) / 2, (vmin_lat + vmax_lat) / 2, 0)
     
    g = geofile.GeoFile('data/hgt15/15-A.tif')
    
    tile = g.get_tile(vmin_lon, vmin_lat, vmax_lon, vmax_lat)
    vertices = tile.get_vertices()
    print('#vertices={0}'.format(len(vertices)))
    # indices = tile.make_mesh_indices()
    indices = tile.make_triangle_indices()
    print('#indices={0}'.format(len(indices)))
    normals = tile.make_normals()
    print('#normals={0}'.format(len(normals)))
    
    print('left={0},bottom={1},right={2},top={3}'.format( \
        tile.get_left(), tile.get_bottom(), \
        tile.get_right(), tile.get_top()))
        
    #pdb.set_trace()
    
    plane = Plane()
    plane.set_eye(eye)
    plane.set_lookAt(lookAt)
    plane.set_up(up)
    
    display = Display('test', width=800, height=800)
    display.create()
    display.set_perspective(90, 1, geofile.meters_to_arc(10), 10000)
    # display.set_ortho(vmin_lon, vmax_lon, vmin_lat, vmax_lat, -10000, 100000)
    
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
        
        eye = plane.get_eye()
        lookAt = plane.get_lookAt()
        up = plane.get_up()
        plane.set_eye((eye[0], eye[1] + geofile.meters_to_arc(50), eye[2]))
        display.lookAt(eye, lookAt, up)
        
        color = (1, 0, 0)
        # display.draw_lines(vertices, indices, normals, color)
        display.draw_triangle_strip(vertices, indices, normals, color)
        
        spos = (-122.295868, 47.8, 0)
        # display.draw_solid_sphere(0.01, 10, 10, (0, 1, 0), center)
        display.postdraw()

        #print(clock.tick())

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
