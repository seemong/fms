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

    g = geofile.GeoFile(sys.argv[1])
    min_lon, min_lat, max_lon, max_lat = g.get_extent()
    print(min_lon, min_lat, max_lon, max_lat)

    display = Display('test', width=800, height=800)
    display.create()

    print("Getting tiles")
    # vmin_lon, vmin_lat, vmax_lon, vmax_lat = (-122.428, 47.48, -122.194, 47.6745)
    vmin_lon, vmin_lat, vmax_lon, vmax_lat = (-121.921155, 46.779471, -121.517574, 46.979085)
    # vmin_lon, vmin_lat, vmax_lon, vmax_lat = (-122.152375, 47.628326, -122.047918, 47.691152)
    t = g.get_tile(vmin_lon, vmin_lat, vmax_lon, vmax_lat)
    
    print("Getting vertices and making indices")
    vertices = t.get_vertices()
    print("Got vertices")
    # vertices, rows, cols = g.get_vertices(vmin_lon, vmin_lat, vmax_lon, vmax_lat)
    mesh_indices = t.make_mesh_indices()
    print("Got mesh indices")
    triangle_indices = t.make_triangle_indices()
    print("Got triangle indices")
    normals = t.make_normals()
    print("Got normals")
    
    """
    vertices = Display.make_vbo(vertices)
    normals = Display.make_vbo(normals)
    triangle_indices = Display.make_numpy_indices(triangle_indices)
    """
    vertices = numpy.array(vertices, 'f')
    normals = numpy.array(normals, 'f')
    triangle_indices = numpy.array(triangle_indices, 'uint32')

    center = ((vmin_lon + vmax_lon) / 2, (vmin_lat + vmax_lat)/2, 0)
    radius = (vmax_lat - vmin_lat)/2
    position = (vmin_lon, vmin_lat, 10, 0.0)
    display.set_light_position(position)
    # display.set_ortho(min_lon, max_lon, min_lat, max_lat, -5000, 50000)
    # display.set_ortho(vmin_lon, vmax_lon, vmin_lat, vmax_lat, -5000, 50000)
    display.set_perspective(90, 1, geofile.meters_to_arc(50), 10000)
    display.lookAt(((vmin_lon + vmax_lon)/2, vmin_lat, \
        geofile.meters_to_arc(4000)), center, (0, 0, 1))

    print(vmin_lon, vmin_lat, vmax_lon, vmax_lat)
    print('center', center)

    clock = pygame.time.Clock()
    theta = 0
    while True:
        quit = False
        for event in display.get_events():
            if event.type == pygame.QUIT:
                quit = True
                break
        if quit:
            break

        x, y = make_eye(radius, theta, center[0], center[1])
        eye = (x, y, geofile.meters_to_arc(3000))
        display.lookAt(eye, center, (0, 0, 1))
        theta += 0.05

        position = (10 * math.sin(theta), -10 * math.cos(theta), 10, 0.0)
        # display.set_light_position(position)

        display.predraw()
        #display.draw_lines(vertices, mesh_indices, normals, (1, 1, 0))
        display.draw_triangle_strip(vertices, triangle_indices, \
            normals, (97.0/256, 51.0/256, 24.0/256))
        spos = (center[0], center[1], 0)
        # display.draw_solid_sphere(0.1, 10, 10, (1, 0, 0), center)
        display.postdraw()

        # print(clock.tick())
        # pygame.time.wait(100)

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
