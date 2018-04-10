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
        eye=(1, 1, 1), center=(0, 0, 0), up = (0, 0, 1),
        ascension=0, near = 0.1, far = 50):
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
        self.eye = eye
        self.center = center
        self.up = up
        assert projection == 'perspective' or projection == 'ortho'
        self.projection = projection
        self.near = near
        self.far = far

        # pygame attributes
        self.screen = None

    def lookAt(self, eye, center, up):
        self.eye = eye
        self.center = center
        self.up = up

        # call open GL
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye[0], eye[1], eye[2],        \
            center[0], center[1], center[2],     \
            up[0], up[1], up[2])


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
        glEnable(GL_CULL_FACE)
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
        ambient = (0.15, 0.15, 0.15, 1.0)      # default is dim white
        diffuse = ( 1.0, 1.0, 1.0, 1.0 )       # default is white light
        position = ( 0.0, 0.0, 0.0 )           # default is origin
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, position)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def set_light_position(self, position):
        """Set the position of the one light in the display"""
        glLightfv(GL_LIGHT0, GL_POSITION, position)

    def get_events(self):
        """Return the pygame events"""
        return pygame.event.get()

    def predraw(self):
        """Call this before drawing frame"""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def postdraw(self):
        """Flip the display as part of postdraw"""
        pygame.display.flip()

    def draw_solid_sphere(self, radius, slices, stacks, color, position):
        """Helper method to draw a solid sphere"""
        glPushMatrix()
        glColor(color)
        glTranslate(position[0], position[1], position[2])
        glutSolidSphere(radius, slices, stacks)
        glPopMatrix()

    def draw_solid_cube(self, size, color, position):
        """Helper method to draw a solid cube"""
        glPushMatrix()
        glTranslate(position[0], position[1], position[2])
        glColor(color)
        glutSolidCube(size)
        glPopMatrix()

if __name__ == '__main__':
    print('Hello World')
    display = Display('test', projection='perspective')
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

        eye = (4 * math.sin(theta), eye[1], eye[2])
        theta += 0.1
        # position = (4 * math.sin(theta), position[1], position[2])
        display.set_light_position(position)
        display.lookAt(eye, center, up)

        display.predraw()
        display.draw_solid_sphere(2, 10, 10, (1, 0, 0), (2, 0, 0))
        display.draw_solid_cube(3, (0, 0, 1), (-2, 0, 0))
        display.postdraw()

    print('Goodbye, World')
