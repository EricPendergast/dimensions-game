import physics
import timer
import time

import pygame
from pygame.locals import *
import math

class Player:
    def __init__(self, pos=None, mass=50):
        self.body = physics.PhysicsBody(pos, mass=mass, mu=0, restitution=0)
        
        self._prevVel = self.body.vel
        
        self._timeSinceJump = timer.Timer()
        
        # How many seconds the player can hold space to keep going up. Lets the
        # player control jump height
        self._maxJumpTime = .3
        self._jumpVel = 5
        
        self._maxVel = 3
        # How fast the player should accelerate when moving on the ground
        self._groundAcc = .17
        # How fast the player should accelerate when in the air
        self._airAcc = .15
        
        self._jumped = False
    
    def render(self, renderer):
        renderer.drawRect(self.body.pos.x , self.body.pos.y , self.body.hitbox.width, self.body.hitbox.height)
    
    def update(self, inputHandler):
        measuredAccel = self.body.vel - self._prevVel
        
       
        inAir = measuredAccel.y < 0
        
        if inputHandler.keyDown(K_SPACE):
            if not self._jumped and not inAir: # start jump
                self.body.vel.y = self._jumpVel
                self._jumped = True
                self._timeSinceJump.start()
            elif self._timeSinceJump.get_time() < self._maxJumpTime and self._jumped:
                # print((self._timeSinceJump.get_time(), self._maxJumpTime))
                self.body.vel.y = self._jumpVel
                
        else:
            self._jumped = False
        
        
        acc = self._airAcc if inAir else self._groundAcc
        
        if inputHandler.keyDown(K_a):
            self.body.acc.x = max(-self._maxVel - self.body.vel.x, -acc)
        elif inputHandler.keyDown(K_d):
            self.body.acc.x = min(self._maxVel - self.body.vel.x, acc)
        else:
            self.body.acc.x = 0
            if not inAir:
                newAcc = acc/2
                self.body.vel.x -= math.copysign(newAcc, self.body.vel.x)
                
                if self.body.vel.x > 0:
                    self.body.vel.x = max(0,  self.body.vel.x - newAcc)
                else:
                    self.body.vel.x = min(0,  self.body.vel.x + newAcc)
            
        self._prevVel = self.body.vel
