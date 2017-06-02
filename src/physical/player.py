import physics

import pygame
from pygame.locals import *

class Player:
    def __init__(self, x = 0, y = 0):
        self.body = physics.PhysicsBody(x,y,0,0)
    
    def render(self, renderer):
        renderer.drawRect(self.body.x , self.body.y , self.body.width, self.body.height)
    
    def update(self, inputHandler):
        print(inputHandler.keyDown(K_a))
        
        if inputHandler.keyDown(K_a):
            self.body.vx = -1
        elif inputHandler.keyDown(K_d):
            self.body.vx = 1
        else:
            self.body.vx = 0
            
        if inputHandler.keyDown(K_s):
            self.body.vy = -1
        elif inputHandler.keyDown(K_w):
            self.body.vy = 1
        else:
            self.body.vy = 0
            
            
        self.body.update()
