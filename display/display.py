from __future__ import print_function
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

vertices = (
    (0, 3, 0), (-2, 2, 0), (-1, 2, 0), (-1, 0, 0),
    (1, 0, 0), (1, 2, 0), (2, 2, 0)
)

edges = (
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)
)

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
)

def draw_diamond():
    glBegin(GL_POLYGON)
    c = 0
    for edge in edges:
        for vertex in edge:
            glColor3fv(colors[c])
            c = (c+1) % len(colors)
            glVertex3fv(vertices[vertex])
    glEnd()
    
def draw_floor():    
    glBegin(GL_LINES)
    glColor3fv((1, 0.5, 0.5))
    for x in range(-10, 11):
        glVertex3fv((x, 0, 10))
        glVertex3fv((x, 0, -10))
        
    for z in range(-10, 11):
        glVertex3fv((10, 0, z))
        glVertex3fv((-10, 0, z))
    glEnd()
    
def draw_sphere():
    glPushMatrix()
    glTranslate(5, 5, -3)
    glColor((0.2, 1, 0.4))
    glutSolidSphere(1, 10, 20)
    glTranslate(2, 2, -2)
    glColor((0.3, 0.3, 0.8))
    glutWireSphere(3, 10, 30)
    glPopMatrix()


def main():
    print("Hello World")

    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glutInit()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    
    x = 10.0
    y = 40.0
    z = 45.0

    rotation_direction = 0
    quit = False
    while not quit:
        delta_x = delta_y = delta_z = 0
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit = True
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rotation_direction = 1
                if event.key == pygame.K_LEFT:
                    rotation_direction = -1
        
        # glRotatef(rotation_direction, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, y, z, 0, 0, 0, x, 1, 0)
        z -= 0.1
        y -= 0.1
        x -= 0.05
 
        draw_diamond()
        draw_floor()
        draw_sphere()

        pygame.display.flip()
        # pygame.time.wait(10)

    pygame.display.quit()
    pygame.quit()
    print("Goodbye World")

if __name__ == "__main__":
    main()
