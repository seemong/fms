from __future__ import print_function
from __future__ import nested_scopes
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays.vbo import *
from OpenGLContext.arrays import *
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
    
def make_normals(count):
    normals = zeros(count, 3)
    for i in range(0, count):
        normals[i] = [0.0, 0.0, 1.0]
    return normals

def main():
    print('Hello World')

    # m = osm.make_osm_map("The Map", sys.argv[1], 20, 1)
    e = Esri(sys.argv[1])
    min_lon, min_lat, max_lon, max_lat = e.get_extent()

    display = dp.Display('test', width=800, height=800)
    display.create()


    eye = (min_lon, min_lat, 2000)
    center = ((min_lon + max_lon) / 2, (min_lat + max_lat)/2, 0)
    otherside = (max_lon, max_lat, 0)
    up = (0, 0, 1)
    print('eye', eye)
    print('center', center)
    print('distance', center[0] - eye[0])
    radius = (max_lat - min_lat) / 2
    
    position = (min_lon, min_lat, 1000)
    # display.set_light_position(position)
    
    # display.set_ortho(min_lon, max_lon, min_lat, max_lat, -5000, 50000)
    display.set_perspective(90, 1, 0.1, 10000)
    display.lookAt(eye, center, up)

    # vertices_vbo = dp.Display.make_vbo(vertices)
    # normals_vbo = dp.Display.make_vbo(normals)
    # indices_idx = dp.Display.make_numpy_indices(indices)

    # vertices = m.get_all_node_coords()
    vertices = VBO(array(e.get_vertices(), 'f'))
    triangle_indices = array(e.get_triangle_indices(), 'uint32')
    # mesh_indices = array(e.get_mesh_indices(), 'uint32')
    normals = VBO(array(e.get_normals(), 'f'))

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
        x, y = make_eye(radius * 2, theta, center[0], center[1])
        eye = (x, y, eye[2])
        position = (1000 * math.sin(theta), -1000 * math.cos(theta), 1000.0, 0.0)
        display.set_light_position(position)
        # display.lookAt(eye, center, up)

        display.predraw()
        # display.draw_solid_cube(3, (0, 0, 1), (-3, 0, 0))
        # for w in m.get_all_ways():
        #    indices = m.get_node_segment_indices_for_way(w)
        #    display.draw_lines(vertices, indices, normals, (1, 1, 0))
        # display.draw_lines(vertices, indices, normals, (1, 1, 0))
        display.draw_triangle_strip(vertices, triangle_indices, normals, (0.7, 0.2, 0.5))
        # display.draw_lines(vertices, mesh_indices, normals, (1, 0, 0))
        spos = (center[0], center[1], 0)
        #display.draw_solid_sphere(500, 10, 10, (1, 0, 0), spos)

        display.postdraw()

        # print(clock.tick(), position)

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
