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
    display = Display('test', width=800, height=800)
    display.create()
    
    """
    vertices = Display.make_vbo(vertices)
    normals = Display.make_vbo(normals)
    triangle_indices = Display.make_numpy_indices(triangle_indices)
    """
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
        #display.draw_lines(vertices, mesh_indices, normals, (1, 1, 0))
        display.draw_triangle_strip(vertices, triangle_indices, \
            normals, (97.0/256, 51.0/256, 24.0/256))
        spos = (center[0], center[1], 0)
        # display.draw_solid_sphere(0.1, 10, 10, (1, 0, 0), center)
        display.postdraw()

        print(clock.tick())

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
