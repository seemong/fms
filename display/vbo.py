from __future__ import print_function
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays.vbo import *
from OpenGLContext.arrays import *
import math

       
def main():
    print("Hello World")

    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    glutInit()
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 5, 1, 0, 0, 0, 1, 0)
    
    vbo = VBO(
            array( [
                [  0, 1, 0 ],
                [ -1,-1, 0 ],
                [  1,-1, 0 ],
                [  2,-1, 0 ],
                [  4,-1, 0 ],
                [  4, 1, 0 ],
                [  2,-1, 0 ],
                [  4, 1, -1 ],
                [  2, 1, -1 ],
            ],'f')
        )
    

    rotation_direction = 0
    quit = False
    while not quit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit = True
                continue
 
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glColor(0, 1, 1)
        vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY);
        glVertexPointerf(vbo)
        glDrawArrays(GL_TRIANGLES, 0, 9)
        vbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        
        #glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(3, 2, -10)
        glColor(1, 1, 0)
        material_color = (0.0, 1.0, 1.0, 1.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, material_color)
        glutSolidSphere(2, 12, 12)
        glPopMatrix()
        
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
