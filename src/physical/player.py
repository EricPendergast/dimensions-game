import physics
import timer

import pygame
from pygame.locals import *

class Player:
    def __init__(self, pos=None, mass=50):
        self.body = physics.PhysicsBody(pos, mass=mass)
        self.prevVel = self.body.vel
        
        self.jumpTimer = timer.Timer()
        # The maximum amout of time between the player releasing the jump
        # button and the player jumping. 
        # Example: if the player releases the jump button a few ticks before
        # they hit the ground, if the length of those few ticks is less than
        # 'timeToJump', the player should jump when they hit the ground
        self.timeToJump = .05
    
    def render(self, renderer):
        renderer.drawRect(self.body.pos.x , self.body.pos.y , self.body.hitbox.width, self.body.hitbox.height)
    
    def update(self, inputHandler):
        accel = self.body.vel - self.prevVel
        
        if inputHandler.keyDown(K_SPACE):
            self.jumpTimer.start()
        
        if accel.y >= 0:
            if self.jumpTimer.get_time() < self.timeToJump:
                self.body.vel.y = 5
                self.jumpTimer.stop()
        
        # if timeToJump
        # print(accel)
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
            
            
        # if inputHandler.keyDown(K_SPACE):
        #     self.body.vel.y = 5
            
        self.prevVel = self.body.vel
