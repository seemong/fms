from __future__ import print_function
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays.vbo import *
from OpenGLContext.arrays import *
import math
import numpy as np
import types

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

    def set_perspective(self, fovy, aspect, zNear, zFar):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, zNear, zFar)

    def set_ortho(self, left, right, bottom, top, near, far):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
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
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # gluPerspective(90, 1, 0.0001, 10000)

        # init lights
        glEnable(GL_LIGHTING)
        # set up light 0
        ambient = (0.15, 0.15, 0.15, 1.0)      # default is dim white
        diffuse = ( 1.0, 1.0, 1.0, 1.0 )       # default is white light
        position = ( 0.0, 0.0, 1.0, 0.0 )      # default is directional from z
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, position)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def set_light_position(self, position):
        """Set the position of the one light in the display"""
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glLightfv(GL_LIGHT0, GL_POSITION, position)
        glPopMatrix()
        """
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

    def quit(self):
        pygame.display.quit()
        pygame.quit()

    @classmethod
    def make_vbo(cls, a):
        """
        Convert a to a VBO from either a regular list, a njmpy array
        or just return a otherwise (assuming it's a VBO)
        """
        if type(a) == types.ListType:
            return VBO(np.array(a, 'f'))
        elif type(a) == np.ndarray:
            return VBO(a)
        else:
            return a

    @classmethod
    def make_numpy_indices(cls, a):
        """
        Convert a to a numpy index if it's a list or just return a
        otherwise
        """
        if type(a) == types.ListType:
            return array(a, 'uint32')
        else:
            return a

    def draw_vertices(self, vertices, indices, normals, color, size, draw_type):
        """Helper method to draw a line"""

        # init
        glColor(color)
        glLineWidth(size)
        glEnableClientState(GL_VERTEX_ARRAY);

        # setup vertices
        vbo = Display.make_vbo(vertices)
        vbo.bind()
        glVertexPointerf(vbo)

        # setup normals
        glEnableClientState(GL_NORMAL_ARRAY)
        vbonorm = Display.make_vbo(normals)
        vbonorm.bind()
        glNormalPointerf(vbonorm)

        indices = Display.make_numpy_indices(indices)
        if draw_type == 'triangles':
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, \
                indices.tostring())
        elif draw_type == 'lines':
            glDrawElements(GL_LINES, len(indices), GL_UNSIGNED_INT, \
                indices.tostring())
        elif draw_type == 'triangle_strip':
            glDrawElements(GL_TRIANGLE_STRIP, len(indices), GL_UNSIGNED_INT, \
                indices.tostring())
                
        # clean up
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    def draw_triangles(self, vertices, indices, normals, color, size=1):
        self.draw_vertices(vertices, indices, normals, color, size, 'triangles')

    def draw_lines(self, vertices, indices, normals, color, size=1):
        self.draw_vertices(vertices, indices, normals, color, size, 'lines')
        
    def draw_triangle_strip(self, vertices, indices, normals, color, size=1):
        self.draw_vertices(vertices, indices, normals, color, size, 'triangle_strip')

if __name__ == '__main__':
    print('Hello World')
    display = Display('test')
    display.create()
    display.set_perspective(90, 1, 0.1, 50)
    display.lookAt((0, 0, 0), (20, 20, 0), (0, 1, 0))
    position = (40, 10, 100, 1.0)
    # display.set_light_position(position)

    eye = (0, 0, 5)
    center = (0, 0, 0)
    up = (0, 0, 1)
    
    vertices = array(               \
        [                           \
                [0.0, 1.0, 0.0],    \
                [1.0, 1.0, 0.0],    \
                [2.0, 1.0, 0.0],    \
                [3.0, 1.0, 0.0],    \
                [0.0, 0.0, 0.0],    \
                [1.0, 0.0, 0.0],    \
                [2.0, 0.0, 0.0],    \
                [3.0, 0.0, 0.0],    \
                [4.0, 0.0, 0.0]     \
        ], 'f')
        
    indices = array([0, 4, 1, 5, 2, 6, 3, 7], 'uint32')
     
        
    normals = array(            \
        [                        \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
                [0.0, 0.0, 1.0], \
        ], 'f')


    eye = (980, 980, 10)
    center = (1000, 1000, 0)
    display.lookAt(eye, center, up)

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
        theta += 0.1
        position = (10 * math.sin(theta), -10 * math.cos(theta), 10, 0.0)
        display.set_light_position(position)
        # display.lookAt(eye, center, up)

        display.predraw()
        display.draw_solid_sphere(2, 10, 10, (1, 0, 0), center)
        # display.draw_solid_cube(2, (0, 0, 1), (-4, 0, 0))
        #display.draw_lines(vertices, indices, normals, \
        #    (0, 1, 0), 2)
        # display.draw_triangle_strip(vertices, indices, normals, (1, 0, 0))
        display.postdraw()

    print('Goodbye, World')
