from __future__ import print_function
from __future__ import nested_scopes
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from geometry.mapobject import *
import display.display as dp
import sys
from numpy import *
import osm.osm as osm
from esri.esri import *

vertices  =                               \
            [
                # 1st triangle
                [  0, 1, 0 ],                  \
                [ -1, 0, 0 ],                  \
                [  1,-0, 0 ],                  \
                # 2nd triangle
                [  0, 0, 0 ],                  \
                [  -2, 0, 2 ],                \
                [  2, 0, 2 ],                 \
            ]

indices = [0, 1, 1, 2, 2, 0, 3, 4, 4, 5, 5, 3]

normals = [                               \
                # 1st triangle
                [0, 0, 1],                    \
                [0, 0, 1],                    \
                [0, 0, 1],                    \
                #2nd triangle
                [0, 1, 0],                    \
                [0, 1, 0],                    \
                [0, 1, 0],                    \
            ]

def make_eye(r, theta, dispx, dispy):
    x = r * math.cos(theta) + dispx
    y = r * math.sin(theta) + dispy
    return x, y

def main():
    print('Hello World')

    # m = osm.make_osm_map("The Map", sys.argv[1], 20, 1)
    e = Esri(sys.argv[1])
    min_lon, min_lat, max_lon, max_lat = e.get_extent()

    display = dp.Display('test', width=1920, height=1080)
    display.create()

    position = (min_lon, min_lat, 4)
    display.set_light_position(position)
    eye = (min_lon, min_lat, 2000)
    center = ((min_lon + max_lon) / 2, (min_lat + max_lat)/2, 0)
    otherside = (max_lon, max_lat, 0)
    up = (0, 0, 1)
    print('eye', eye)
    print('center', center)
    print('distance', center[0] - eye[0])
    radius = (max_lat - min_lat) / 2

    # display.set_ortho(min_lon, max_lon, min_lat, max_lat, -5000, 50000)
    display.set_perspective(90, 1, 0.1, 10000)
    display.lookAt(eye, center, up)

    # vertices_vbo = dp.Display.make_vbo(vertices)
    # normals_vbo = dp.Display.make_vbo(normals)
    # indices_idx = dp.Display.make_numpy_indices(indices)

    # vertices = m.get_all_node_coords()
    vertices = e.vertices()

    clock = pygame.time.Clock()

    theta = 0
    delta_x = 100
    while True:
        quit = False
        for event in display.get_events():
            if event.type == pygame.QUIT:
                quit = True
                break
        if quit:
            break

        # eye = (4 * math.sin(theta), 4 * math.cos(theta) , eye[2])
        theta += 0.1
        # eye = (eye[0] + delta_x, eye[1], eye[2])
        x, y = make_eye(radius, theta, center[0], center[1])
        eye = (x, y, eye[2])
        # display.set_light_position(position)
        # display.lookAt(eye, center, up)

        display.predraw()
        # display.draw_solid_cube(3, (0, 0, 1), (-3, 0, 0))
        # for w in m.get_all_ways():
        #    indices = m.get_node_segment_indices_for_way(w)
        #    display.draw_lines(vertices, indices, normals, (1, 1, 0))
        indices = e.indices()
        display.draw_lines(vertices, indices, normals, (1, 1, 0))
        display.draw_solid_sphere(10, 10, 10, (1, 0, 0), center)


        display.postdraw()

        # print(clock.tick())

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
