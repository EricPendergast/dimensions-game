from OpenGL.GL import *
from OpenGL.GLU import *

class Renderer:
    def drawRect(self, x, y, w, h):
        glColor((255,255,255))
        glBegin(GL_QUADS)

        glVertex((x,y,0))
        glVertex((x+w,y,0))
        glVertex((x+w,y+h,0))
        glVertex((x,y+h,0))

        glEnd()
