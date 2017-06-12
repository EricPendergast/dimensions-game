import player
# import physics
from physics import *
import simple_entity

import settings
# import json
import pickle as json

import math

class Level:
    def __init__(self):
        # grid contains all the blocks in the current level. If a coordinate is
        # not one of the keys in grid, it is assumed to be air
        self.grid = {}
        self.load("1.lvl")
        
        # self.grid[Vec(1,1)] = 1
        # self.grid[Vec(14,1)] = 1
        self.entities = []
        self.player = player.Player(Vec(40,40), mass=50)
        self.entities.append(self.player)
        
        for i in range(5):
            self.entities.append(
                    simple_entity.SimpleEntity(
                    PhysicsBody(Vec(200,200 + 50*i))))
        
        self._render_queue_debug = []
        self.physics = PhysicsEnacter()
        # self.save("1.lvl")
        
        for key in self.grid:
            assert(type(key) is Vec)
    
    def render(self, renderer):
        for square in self.grid:
            renderer.drawAABB(self._get_grid_physics_body(square).hitbox)
        
        for entity in self.entities:
            entity.render(renderer)
    
        while self._render_queue_debug:
            renderer.drawAABB(self._render_queue_debug.pop())
    
    def update(self, inputHandler):
        self.player.update(inputHandler)
        
        # self.physics.enact_single(self.player.body)
        # self.physics.enact_single(self.body1)
        for entity in self.entities:
            self.physics.enact_single(entity.body)
        
        for i in range(1):
            for entityA in self.entities:
                for entityB in self.entities:
                    if not entityA is entityB:
                        self.physics.enact_pair(entityA.body, entityB.body)
                        
                self._collide_with_grid(entityA.body)
    
    
        
    # returns the physics body of the block in the grid with location 'pos'
    def _get_grid_physics_body(self, pos):
        
        assert type(pos) is Vec
        
        ret = PhysicsBody(hitbox=AABB())
        # if pos is not in the grid, it is air
        if pos in self.grid:
            ret.hitbox.max = Vec(settings.GRID_SIZE, settings.GRID_SIZE)
            ret.pos = pos*settings.GRID_SIZE
            ret.mass = 1000000
            
        return ret
    
    
    def save(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "w")
        file.write(json.dumps(self.grid))
        
    def load(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "r")
        self.grid = json.loads(file.read())
    
    def _collide_with_grid(self, body):
        assert type(body) is PhysicsBody
        for block_pos in self.grid:
            block_body = self._get_grid_physics_body(block_pos)
            
            manifold = body.hitbox.get_manifold(block_body.hitbox)
            
            if manifold.depth <= 0:
                continue
            # This is to prevent snagging when walking on blocks that are in a
            # row. If the collision is valid and the collision would push the
            # player in the direction of an adjacent block, the collision
            # should not occur. This is because this situation causes the
            # player to move in a way that would not happen in real physics
            if (block_pos + manifold.normal in self.grid):
                continue
            
            self.physics.enact_pair(body, block_body)
            
    
    # def _collide_with_grid(self, body):
    #     assert type(body) is PhysicsBody
    #     # [bottom, up, right, left]
    #     dirs = [Vec(1,0), Vec(-1,0), Vec(0,1), Vec(0,-1)]
    #
    #     for i in range(3):
    #
    #         if i==0: #collide with block below
    #             collide_block = Vec((body.hitbox.min.x+body.hitbox.max.x)/2,
    #                 body.hitbox.min.y) / settings.GRID_SIZE
    #             collide_block.x = math.floor(collide_block.x)
    #             collide_block.y = round(collide_block.y)-1
    #         elif i==1: #collide with block above
    #             collide_block = Vec((body.hitbox.min.x+body.hitbox.max.x)/2,
    #                 body.hitbox.max.y) / settings.GRID_SIZE
    #             collide_block.x = math.floor(collide_block.x)
    #             collide_block.y = round(collide_block.y)
    #         elif i==2: #collide with block to the right
    #             collide_block = Vec(body.hitbox.max.x,
    #                 (body.hitbox.min.y+body.hitbox.max.y)/2) / settings.GRID_SIZE
    #             collide_block.x = round(collide_block.x)
    #             collide_block.y = math.floor(collide_block.y)
    #
    #
    #
    #         if collide_block in self.grid:
    #             print("HERE")
    #             self.physics.enact_pair(body,
    #                     self._get_grid_physics_body(collide_block))
    #
    #             self._render_queue_debug.append(
    #                     self._get_grid_physics_body(collide_block).hitbox)
    #         elif i <= 1:
    #             print("NOT HERE")
    #             collide_block -= dirs[i]
    #             self.physics.enact_pair(body,
    #                     self._get_grid_physics_body(collide_block))
    #             self._render_queue_debug.append(
    #                     self._get_grid_physics_body(collide_block).hitbox)
    #
    #             collide_block += dirs[i]*2
    #             self.physics.enact_pair(body,
    #                     self._get_grid_physics_body(collide_block))
    #             self._render_queue_debug.append(
    #                     self._get_grid_physics_body(collide_block).hitbox)
    #         else:
    #             collide_block -= dirs[i]
    #
    #
