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
            
def _connect_indices(indices):
    result = []
    for i in range(0, len(indices)):
        result.append(indices[i])
        if i > 0 and i < len(indices) - 1:
            result.append(indices[i])
    return result


def main():
    print('Hello World')
    
    m = osm.make_osm_map("The Map", sys.argv[1])
    min_lon, min_lat, max_lon, max_lat = m.get_extent()
        
    display = dp.Display('test', projection='ortho')
    display.create()
    
    display.set_ortho(min_lon, max_lon, min_lat, max_lat, -50, 50)

    position = (min_lon, min_lat, 4)
    display.set_light_position(position)
    eye = ((min_lon + max_lon) / 2, (min_lat + max_lat)/2, 10)
    center = ((min_lon + max_lon) / 2, (min_lat + max_lat)/2, 0)
    up = (0, 0, 1)
    print('eye', eye)
    print('center', center)
    radius = (max_lat - min_lat) / 2

    # vertices_vbo = dp.Display.make_vbo(vertices)
    # normals_vbo = dp.Display.make_vbo(normals)
    # indices_idx = dp.Display.make_numpy_indices(indices)
    
    vertices = m.get_all_node_coords()
        
    theta = 0
    while True:
        quit = False
        for event in display.get_events():
            if event.type == pygame.QUIT:
                quit = True
                break
        if quit:
            break

        # eye = (4 * math.sin(theta), 4 * math.cos(theta) , eye[2])
        # theta += 0.1
        # position = (4 * math.sin(theta), -4 * math.cos(theta), position[2])
        # display.set_light_position(position)
        # display.lookAt(eye, center, up)

        display.predraw()
        # display.draw_solid_sphere(radius, 10, 10, (1, 0, 0), center)
        # display.draw_solid_cube(3, (0, 0, 1), (-3, 0, 0))
        for w in m.get_all_ways():
            indices = _connect_indices(m.get_node_indices_for_way(w))
            display.draw_lines(vertices, indices, normals, (0, 1, 1))
        display.postdraw()

    display.quit()
    print('Goodbye, World')

if __name__ == '__main__':
    main()
