from __future__ import print_function
from __future__ import nested_scopes
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from PIL import Image

def load_texture(name):
    im = Image.open("download.jpg")
    ix, iy, image = im.size[0], im.size[1], im.tobytes('raw', "RGBX", 0, -1)  
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    return ID
   
def draw_sphere(r, x, y, z, c):
    glPushMatrix()
    glTranslate(x, y, z)
    glColor(c)
    glutSolidSphere(r, 10, 10)
    glPopMatrix()  


def make_render_frame():
    texture_id = load_texture("download.jpg")
    
    def render_frame():        
        draw_sphere(1, 2, 1, -4, (1, 0.3, 0.2))
        draw_sphere(2, -1, -2, 3, (0.3, 0.2, 0.7))
        draw_cube(texture_id)
        
    return render_frame

def draw_cube(id):
    """Draw a cube with texture coordinates"""
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glBindTexture(GL_TEXTURE_2D, id)
    
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
        
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0,  1.0)
        
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0,  1.0)
        
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0,  1.0)
        
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
        
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0,  1.0, -1.0)
        
    glTexCoord2f(0.0, 1.0)
    glVertex3f( 1.0,  1.0, -1.0)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3f( 1.0, -1.0, -1.0)
        
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0, -1.0)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0,  1.0,  1.0)
        
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0,  1.0,  1.0)
        
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0, -1.0)
        
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
        
    glTexCoord2f(0.0, 1.0)
    glVertex3f( 1.0, -1.0, -1.0)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3f( 1.0, -1.0,  1.0)
        
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
        
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0, -1.0)
        
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0, -1.0)
        
    glTexCoord2f(0.0, 1.0)
    glVertex3f( 1.0,  1.0,  1.0)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3f( 1.0, -1.0,  1.0)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
        
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
        
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0,  1.0,  1.0)
        
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def init_gl():
    glutInit()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (10, -5, 10))

def main():
    print("Hello World")

    pygame.init()
    display = (800, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    init_gl()
    
    x = 2
    y = 2
    z = 10
    render_func = make_render_frame()

    quit = False
    while not quit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit = True
                continue
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)
        z -= 0.1
        
        render_func()
        pygame.display.flip()
       
    pygame.display.quit()
    pygame.quit()
    print("Goodbye World");
        
 
if __name__ =="__main__":
    main()
