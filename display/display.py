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
        width=800, height=800, redraw_func=None, perspective=True,
        eye=(0, 0, 0), heading=0, ascension=0):
        """
        Name describes this display object.
        Position is the position of the display in window coordinates
        Width and height of the pygame display
        """
        self.name = name
        self.display = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.perspective = perspective
        
        self.redraw_func = None
        
        # pygame attributes
        self.screen = None
        
        # set camera
        lookAt(eye, heading, ascension)
        
    def lookAt(eye, heading, ascension):
        self.eye = eye
        self.heading = heading
        self.ascension = ascension
        #TODO(calculate look at point)
        
    def ortho(left, right, bottom, top, near, far):
        glOrtho(left, right, bottom top, near, far)
        
    def set_redraw_func(self, redraw_func):
        """
        Set the redrawing function
        """
        self.redraw_func = redraw_func
        
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
        if self.perspective:
            gluPerspective(90, 1, 0.1, 100)
        else:
            glOrtho(-4, 4, -4, 4, 0.1, 50)
        
        # init lights
        glEnable(GL_LIGHTING)
        # set up light 0
        ambient = (0.2, 0.2, 0.2, 1.0)      # default is dim white
        diffuse = ( 1.0, 1.0, 1.0, 1.0 )    # default is white light
        position = ( 0.0, 0.0, 0.0 )        # default is origin
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
        glLightfv(GL_LIGHT0, GL_POSITION, position);
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        
    def get_events(self):
        return pygame.event.get()

    def redraw(self):
        """Draw one frame"""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # call the redrawing function
        self.redraw_func(self)

if __name__ == '__main__':
    def redraw(display):
        pass
        
    
    display = Display("test-display")
    
