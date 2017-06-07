import physics

import pygame
from pygame.locals import *

class Player:
    def __init__(self, pos=None, mass=50):
        self.body = physics.PhysicsBody(pos, mass=mass)
    
    def render(self, renderer):
        renderer.drawRect(self.body.pos.x , self.body.pos.y , self.body.hitbox.width, self.body.hitbox.height)
    
    def update(self, inputHandler):
        
        # if inputHandler.keyDown(K_a):
        #     self.body.vel.x = -1
        # elif inputHandler.keyDown(K_d):
        #     self.body.vel.x = 1
        # else:
        #     self.body.vel.x = 0
        #
        # if inputHandler.keyDown(K_s):
        #     self.body.vel.y = -1
        # elif inputHandler.keyDown(K_w):
        #     self.body.vel.y = 1
        # else:
        #     self.body.vel.y = 0
        if inputHandler.keyDown(K_a):
            self.body.acc.x = -.1
        elif inputHandler.keyDown(K_d):
            self.body.acc.x = .1
        else:
            self.body.acc.x = 0
            
        if inputHandler.keyDown(K_s):
            self.body.acc.y = -.1
        elif inputHandler.keyDown(K_w):
            self.body.acc.y = .1
        else:
            self.body.acc.y = 0
            
            
        if inputHandler.keyDown(K_SPACE):
            self.body.vel.y = 5
            
