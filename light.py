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
    array(
        [
            # 1st triangle
            [  0, 1, 0 ],
            [ -1, 0, 0 ],
            [  1,-0, 0 ],
            # 2nd triangle
            [  0, 0, 0 ],
            [  -2, 0, 2 ],
            [  2, 0, 2 ],
        ],'f')
)

vertex_indices = array(
    [0, 1, 1, 2, 2, 0], 'uint32')


normals = VBO(
    array(
        [
            # 1st triangle
            [0, 0, 1],
            [0, 0, 1],
            [0, 0, 1],
            #2nd triangle
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ], 'f')
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
    glEnable(GL_CULL_FACE)
    glShadeModel(GL_SMOOTH)

    # init lights
    glEnable(GL_LIGHTING)
    # set up light 0
    ambient = (0.2, 0.2, 0.2, 1.0)
    diffuse = ( 1.0, 1.0, 1.0, 1.0 )
    position = ( 0.0, 10.0, 2.0, 1.0 )
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
    glLightfv(GL_LIGHT0, GL_POSITION, position);
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)

    # set projection transform
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    # glOrtho(-2, 2, -2, 2, 0.1, 50)

    # set viewingtransform
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 5, 5, 0, 0, 0, 0, 1, 0)
    
    x = 20
    y = 10
    z = 10
    theta = 0

    clock = pygame.time.Clock()

    quit = False
    while not quit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit = True
                    break

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # set viewingtransform
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        #gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)

        theta += 0.01
        x = 5 * math.sin(theta)
        z = 5 * math.cos(theta)

        glPushMatrix()
        glColor(0, 0, 1)
        glTranslate(-3, 0, -2)
        glutSolidSphere(2, 50, 40)
        glPopMatrix()


        glPushMatrix()
        glTranslate(2, 2, -4)
        glColor(1.0, 0.0, 0.0)
        glutSolidCube(2)
        glPopMatrix()

        glColor(1.0, 1.0, 0.0)
        glEnableClientState(GL_VERTEX_ARRAY);
        vbo.bind()
        glVertexPointerf(vbo)

        glEnableClientState(GL_NORMAL_ARRAY)
        normals.bind()
        glNormalPointerf(normals)

        # glDrawArrays(GL_TRIANGLES, 0, 6)
        # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, vertex_indices.tostring())
        glDrawElements(GL_LINES, 6, GL_UNSIGNED_INT, vertex_indices.tostring())

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        pygame.display.flip()
        print(clock.tick())
        # pygame.time.wait(50)

    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    main()
