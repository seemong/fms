from __future__ import print_function
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class Display(object):
    """
    Display object combines pygame and pyopengl to provide a
    double buffered drawing surface for 2D/3D
    """

    def __init__(self, name = "", x=0, y=0,
        width=800, height=800, projection="perspective",
        eye=(0, 0, 0), true_heading=0, ascension=0):
        """
        Name describes this display object.
        Position is the position of the display in window coordinates.
        Width and height of the pygame display.
        Heading in true degrees, ascension in degrees.
        """
        self.name = name
        self.display = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.true_heading = true_heading
        self.ascension = ascension
        assert projection == 'perspective' or projection == 'ortho'
        self.projection = projection

        # pygame attributes
        self.screen = None

        # set camera
        self.lookAt(eye, true_heading, ascension)

    def lookAt(self, eye, true_heading, ascension):
        self.eye = eye
        self.true_heading = true_heading
        self.ascension = ascension
        #TODO(calculate look at point)

    def set_perspective(fovy, aspect, zNear, zFar):
        glMatrixMode(GL_PROJECTION)
        gluPerpective(fovy, aspect, zNear, zFar)

    def ortho(left, right, bottom, top, near, far):
        glMatrixMode(GL_PROJECTION)
        glOrtho(left, right, bottom, top, near, far)

    def create(self):
        """Initialize and create display on the screen"""

        # init pygame
        pygame.init()
        size = (self.width, self.height)
        self.screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

        #init GL
        glutInit()
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_CULL_FACE)
        glShadeModel(GL_SMOOTH)

        # init projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.projection == 'perspective' :
            gluPerspective(90, 1, 0.1, 100)
        else:
            glOrtho(-4, 4, -4, 4, 0.1, 50)

        # init lights
        glEnable(GL_LIGHTING)
        # set up light 0
        ambient = (0.2, 0.2, 0.2, 1.0)      # default is dim white
        diffuse = ( 1.0, 1.0, 1.0, 1.0 )    # default is white light
        position = ( 0.0, 10.0, 2.0 )        # default is origin
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
        glLightfv(GL_LIGHT0, GL_POSITION, position);
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def get_events(self):
        return pygame.event.get()

    def predraw(self):
        """Call this before drawing frame"""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def postdraw(self):
        """Flip the display as part of postdraw"""
        pygame.display.flip()

    def draw_solid_sphere(self, radius, slices, stacks, color, position):
        glPushMatrix()
        glColor(color)
        glTranslate(position[0], position[1], position[2])
        glutSolidSphere(radius, slices, stacks)
        glPopMatrix()

if __name__ == '__main__':
    print('Hello World')
    display = Display('test', projection='ortho')
    display.create()
    while True:
        quit = False
        for event in display.get_events():
            if event.type == pygame.QUIT:
                quit = True
                break
        if quit:
            break

        display.predraw()
        display.draw_solid_sphere(2, 10, 10, (1, 0, 0), (0, 0, 0))
        display.postdraw()

    print('Goodbye, World')
