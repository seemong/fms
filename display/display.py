from __future__ import print_function
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (0, 1, 0), (-1, 0, 0), (0, -1, 0), (1, 0, 0)
)

edges = (
    (0, 1), (1, 2), (2, 3), (3, 0)
)

def draw_diamond():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    print("Hello World")

    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(45, 1, 0.1, 10)
    
    x = 0.0
    y = 0.0
    z = -5.0
    glTranslatef(x, y, z)
 
    while True:
        delta_x = delta_y = delta_z = 0
        
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                delta_x = -0.1
            if event.key == pygame.K_LEFT:
                delta_x = 0.1
            if event.key == pygame.K_UP:
                delta_y = -0.1
            if event.key == pygame.K_DOWN:
                delta_y = 0.1
            if event.key == pygame.K_q:
                delta_z = 0.1
            if event.key == pygame.K_a:
                delta_z = -0.1
                
        glTranslatef(delta_x, delta_y, delta_z)
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_diamond()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.display.quit()
    pygame.quit()
    print("Goodbye World")

if __name__ == "__main__":
    main()
