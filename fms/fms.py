from __future__ import print_function
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

vertices  =  array(                               \
            [
                # 1st triangle
                [  0, 1, 0 ],                  \
                [ -1, 0, 0 ],                  \
                [  1,-0, 0 ],                  \
                # 2nd triangle
                [  0, 0, 0 ],                  \
                [  -2, 0, 2 ],                \
                [  2, 0, 2 ],                 \
            ], 'f')

indices = array([0, 1, 2, 3, 4, 5], 'uint32')

normals = array([                               \
                # 1st triangle
                [0, 0, 1],                    \
                [0, 0, 1],                    \
                [0, 0, 1],                    \
                #2nd triangle
                [0, 1, 0],                    \
                [0, 1, 0],                    \
                [0, 1, 0],                    \
            ], 'f')


def main():
    print('Hello World')
    display = dp.Display('test', projection='perspective')
    display.create()

    position = (-4, 4, 4)
    display.set_light_position(position)
    eye = (-4, -5, 5)
    center = (0, 0, 0)
    up = (0, 0, 1)

    theta = 0
    while True:
        quit = False
        for event in display.get_events():
            if event.type == pygame.QUIT:
                quit = True
                break
        if quit:
            break

        eye = (4 * math.sin(theta), 4 * math.cos(theta) , eye[2])
        theta += 0.1
        position = (4 * math.sin(theta), -4 * math.cos(theta), position[2])
        display.set_light_position(position)
        display.lookAt(eye, center, up)

        display.predraw()
        display.draw_solid_sphere(2, 10, 10, (1, 0, 0), (3, 0, 0))
        display.draw_solid_cube(3, (0, 0, 1), (-3, 0, 0))
        display.draw_triangles(vertices, indices, normals, (0, 1, 1))
        display.postdraw()

    print('Goodbye, World')

if __name__ == '__main__':
    main()
