from OpenGL.GL import *
from OpenGL.GLU import *

# Encapsulates OpenGL rendering
class Renderer:
    def begin_quads(self):
        glBegin(GL_QUADS)
    
    def end(self):
        glEnd()
        
    def drawRect(self, x, y, w, h, color=(255,255,255), begin=True):
        glColor(color)
        if begin:
            glBegin(GL_QUADS)
        
        glVertex((x,y,0))
        glVertex((x+w,y,0))
        glVertex((x+w,y+h,0))
        glVertex((x,y+h,0))
        
        if begin:
            glEnd()
        
    def drawAABB(self, aabb, begin=True):
        self.drawRect(aabb.min.x, aabb.min.y, aabb.width, aabb.height, begin=begin)
