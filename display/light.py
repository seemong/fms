from __future__ import print_function
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays.vbo import *
from OpenGLContext.arrays import *
import math

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
       
def main():
    print("Hello World")

    # init pygame
    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    #init GL
    glutInit()
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    
    # set projection transform
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    
    # set viewingtransform
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)
    
    # init lights
    glEnable(GL_LIGHTING)
    # set up light 0
    ambient = (0.1, 0.1, 0.1, 1.0)
    diffuse = ( 1.0, 1.0, 1.0, 1.0 )
    position = ( 5.0, 5.0, 5.0 )
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
    glLightfv(GL_LIGHT0, GL_POSITION, position);  
    glColorMaterial(GL_FRONT, GL_DIFFUSE) 
    glEnable(GL_COLOR_MATERIAL)
    
    quit = False
    while not quit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit = True
                break
 
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glColor(0, 0, 1)
        glutSolidSphere(2, 50, 40)
        # glutSolidCube(2)
        
        glTranslate(2, 2, -4)
        glColor(1.0, 0.0, 0.0)
        glutSolidCube(2)
        glPopMatrix()
        
        vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY);
        glColor(1.0, 1.0, 0.0)
        glVertexPointerf(vbo)
        glDrawArrays(GL_TRIANGLES, 0, 9)
        vbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        
        pygame.display.flip()
        # pygame.time.wait(100)
        
if __name__ == "__main__":
    main()
