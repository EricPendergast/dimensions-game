import player
# import physics
from physics import *
from integer_physics import *
import simple_entity

import settings
# import json
import pickle as json

import math

# Handles map rendering and storage
class Level:
    def __init__(self):
        # grid contains all the blocks in the current level. If a coordinate is
        # not one of the keys in grid, it is assumed to be air
        self.grid_update_period = 50
        # Incremented by 1 each tick
        self.ticker = 0
        
        self.grid = Grid()
        
        init_in_grid(self.grid.current, Vec(2,2), GravityBlock, Vec(5,5))
        
        # self.grid[Vec(20,1)] = 1
        # self.grid[Vec(26,1)] = 1
        # self.grid[Vec(32,1)] = 1
        # self.grid[Vec(41,1)] = 1
        self.player = player.Player(Vec(40,70), mass=5)
        
        # self._render_queue_debug = []
        self.physics = PhysicsEnacter()
        # self.save("1.lvl")
    
    
    def render(self, renderer):
        self.grid.render(renderer)
        
        self.player.render(renderer)
    
    
    def update_player(self, inputHandler):
        self.ticker = self.ticker+1
        self.player.update(inputHandler)
        
        self.physics.enact_single(self.player.body)
        
        self._collide_with_grid(self.player.body)
    
        if self.ticker % self.grid_update_period == 0:
            self.grid.update()
   
    
    def save(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "w")
        file.write(json.dumps(self.grid))
        
    def load(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "r")
        self.grid = json.loads(file.read())
    
    def _collide_with_grid(self, body):
        assert type(body) is PhysicsBody
        
        center_x = int(self.player.body.pos.x)/settings.GRID_SIZE
        center_y = int(self.player.body.pos.y)/settings.GRID_SIZE
        block_pos = Vec(0,0)
        for x in xrange(center_x - 5, center_x + 5):
            for y in xrange(center_y - 5, center_y + 5):
                block_pos.x, block_pos.y = x,y
                
                if not self.grid.contains_block(block_pos):
                    continue
                
                block_body = self.grid._get_physics_body(block_pos)
                
                manifold = body.hitbox.get_manifold(block_body.hitbox)
                
                if manifold.depth <= 0:
                    continue
                
                # Prevents snagging when walking on blocks that are in a row.
                # If the collision is valid and the collision would push the player
                # in the direction of an adjacent block, the collision should not
                # occur.
                if (self.grid.contains_block(block_pos + manifold.normal)):
                    continue
                
                self.physics.enact_pair(body, block_body)
            


class Grid(object):
    def __init__(self):
        self.width = 20
        self.height = 20
        
        self.current = [[Block(Air, pos=Vec(j,i)) for i in range(self.height)] for j in range(self.width)]
        self.future_buckets = self.FutureBuckets(self.width, self.height)
        
        # Block(self.current, Vec(2,1))
        
    
    def contains_block(self, pos):
        return pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height and \
                (self.current[int(pos.x)][int(pos.y)].BlockType is not Air)
                
    def update(self):
        self.future_buckets.clear()
        # sending each block in 'current' to buckets in 'future_buckets'
        for x in xrange(self.width):
            for y in xrange(self.height):
                block = self.current[x][y]
                if block is not None:
                    block.update(self.current, self.future_buckets)
                    
        # clearing 'current'
        for x in xrange(self.width):
            for y in xrange(self.height):
                self.current[x][y].init(Air)
        
        # Each bucket contains multiple blocks, so each needs to be collapsed
        # into just one before it is put into 'current'
        for x in xrange(self.width):
            for y in xrange(self.height):
                 self.future_buckets._buckets_mat[x][y].collapse(self.current[x][y])
                    
                    
    def render(self, renderer):
        renderer.begin_quads()
        for x in xrange(self.width):
            for y in xrange(self.height):
                block = self.current[x][y]
                if block.BlockType is not Air:
                    # assert issubclass(type(block), Block)
                    renderer.drawAABB(self._get_physics_body(block.pos).hitbox, False)
        renderer.end()
        
        
    # returns the physics body of the block in the grid with location 'pos'
    def _get_physics_body(self, pos):
        ret = PhysicsBody(hitbox=AABB())
        
        if self.current[int(pos.x)][int(pos.y)] is not None:
            ret.hitbox.max = Vec(settings.GRID_SIZE, settings.GRID_SIZE)
            ret.pos = pos*settings.GRID_SIZE
            ret.mass = 1000000
            
        return ret
 
    class FutureBuckets(object):
        def __init__(self, width, height):
            self.width = width;
            self.height = height;
            self._buckets_mat = [[BlockBucket(Vec(j,i)) for i in range(self.height)] for j in range(self.width)]
            
        def put(self, pos, BlockType, *args, **kwargs):
            if self.in_range(pos):
                self._buckets_mat[int(pos.x)][int(pos.y)].put(BlockType, *args, **kwargs)
        
        def clear(self):
            for x in xrange(self.width):
                for y in xrange(self.height):
                    self._buckets_mat[x][y].clear()
                    
        def in_range(self, pos):
            return pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height
        
        def __repr__(self):
            return str(self._buckets_mat)
