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

def draw_diamond():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
def draw_floor():
    glBegin(GL_LINES)
    for x in range(-10, 11):
        glVertex3fv((x, 0, 10))
        glVertex3fv((x, 0, -10))
        
    for z in range(-10, 11):
        glVertex3fv((10, 0, z))
        glVertex3fv((-10, 0, z))
    glEnd()
    



def main():
    print("Hello World")

    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    
    x = 0.0
    y = 0.0
    z = 5.0
    # glTranslatef(x, y, z)
    #print_mv()
    # gluLookAt(0, 3, 5, 0, 0, 0, 0, 1, 0)
    #print_mv()
 
    rotation_direction = 0
    quit = False
    while not quit:
        delta_x = delta_y = delta_z = 0
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit = True
                continue
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rotation_direction = 1
                if event.key == pygame.K_LEFT:
                    rotation_direction = -1
        
        # glRotatef(rotation_direction, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, y, z, 0, 0, 0, 0, 1, 0)
        z += 0.1
        y += 0.1
 
        draw_diamond()
        draw_floor()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.display.quit()
    pygame.quit()
    print("Goodbye World")

if __name__ == "__main__":
    main()
