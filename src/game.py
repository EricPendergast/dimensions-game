from math import radians 

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import settings
import state_manager
import renderer
import input

def init():
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    
    
def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width/settings.SCALE, 0, height/settings.SCALE, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
# def render(counter):
#     glColor((255,255,255))
#     glBegin(GL_QUADS)
#
#     glVertex((counter,0,0))
#     glVertex((100,0,0))
#     glVertex((100,100,0))
#     glVertex((0,100,0))
#
#     glEnd()
    
def run():
    
    pygame.init()
    screen = pygame.display.set_mode(settings.SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    
    resize(*settings.SCREEN_SIZE)
    
    clock = pygame.time.Clock()
    
    stateManager = state_manager.StateManager()
    
    # Encapsulates OpenGL rendering
    renderHandler = renderer.Renderer()
    
    # Encapsulates input from keyboard and (eventually) mouse
    inputHandler = input.InputHandler()
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                return
        
        if inputHandler.keyDown(K_RETURN) | inputHandler.keyDown(K_ESCAPE):
            return
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        stateManager.render(renderHandler)
        stateManager.update(inputHandler)
        
        
        pygame.display.flip()
        
        clock.tick(settings.FRAMERATE)
        
        
run()
