import physics
import timer

import pygame
from pygame.locals import *
import math

class Player:
    def __init__(self, pos=None, mass=50):
        self.body = physics.PhysicsBody(pos, mass=mass, mu=0)
        self.prevVel = self.body.vel
        
        # self.jumpTimer = timer.Timer()
        # The maximum amout of time between the player releasing the jump
        # button and the player jumping. 
        # Example: if the player releases the jump button a few ticks before
        # they hit the ground, if the length of those few ticks is less than
        # 'timeToJump', the player should jump when they hit the ground
        self.timeToJump = .03
        self.timeSinceJump = timer.Timer()
        
        # How many seconds the player can hold space to keep going up. Lets the
        # player control jump height
        self.maxJumpTime = .5
        self.jumpVel = 5
        
        self.maxVel = 3
        # How fast the player should accelerate when moving on the ground
        self.groundAcc = .2
        # How fast the player should accelerate when in the air
        self.airAcc = .15
        
        self.jumped = False
    
    def render(self, renderer):
        renderer.drawRect(self.body.pos.x , self.body.pos.y , self.body.hitbox.width, self.body.hitbox.height)
    
    def update(self, inputHandler):
        measuredAccel = self.body.vel - self.prevVel
        
        
       
        inAir = measuredAccel.y < 0
        
        if inputHandler.keyDown(K_SPACE):
            if not self.jumped and not inAir: # start jump
                self.body.vel.y = self.jumpVel
                self.jumped = True
                self.timeSinceJump.start()
            elif self.timeSinceJump.get_time() < self.timeToJump:
                self.body.vel.y = self.jumpVel
                
        else:
            self.jumped = False
        
        
        acc = self.airAcc if inAir else self.groundAcc
        
        if inputHandler.keyDown(K_a):
            self.body.acc.x = max(-self.maxVel - self.body.vel.x, -acc)
            
        elif inputHandler.keyDown(K_d):
            self.body.acc.x = min(self.maxVel - self.body.vel.x, acc)
            
        else:
            self.body.acc.x = 0
            if not inAir:
                newAcc = acc/2
                self.body.vel.x -= math.copysign(newAcc, self.body.vel.x)
                if self.body.vel.x > 0:
                    self.body.vel.x = max(0,  self.body.vel.x - newAcc)
                else:
                    self.body.vel.x = min(0,  self.body.vel.x + newAcc)
                    
            
            
        self.prevVel = self.body.vel
