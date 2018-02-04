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
        
        # self.grid[Vec(20,1)] = 1
        # self.grid[Vec(26,1)] = 1
        # self.grid[Vec(32,1)] = 1
        # self.grid[Vec(41,1)] = 1
        self.player = player.Player(Vec(40,70), mass=5)
        
        # self._render_queue_debug = []
        self.physics = PhysicsEnacter()
        # self.save("1.lvl")
        
        for key in self.grid.current:
            assert(type(key) is Vec)
    
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
        for block_pos in self.grid.current:
            block_body = self.grid._get_physics_body(block_pos)
            
            manifold = body.hitbox.get_manifold(block_body.hitbox)
            
            if manifold.depth <= 0:
                continue
            
            # Prevents snagging when walking on blocks that are in a row.
            # If the collision is valid and the collision would push the player
            # in the direction of an adjacent block, the collision should not
            # occur.
            if (block_pos + manifold.normal in self.grid.current):
                continue
            
            self.physics.enact_pair(body, block_body)
            

# grid contains all the blocks in the current level. If a coordinate is
# not one of the keys in grid, it is assumed to be air
class Grid(object):
            
    def __init__(self):
        self._grids = [{}, {}]
        self._current_grid = 0
        
        self.valid_area = (0,0,100,100)
        self.future_buckets = self.FutureBuckets(self.valid_area[2], self.valid_area[3])
        
        # Block(self.current, Vec(2,1))
        GravityBlock(self.current, Vec(2,2), Vec(5,5))
        
        for key in self.current:
            assert(type(key) is Vec)
    
    def update(self):
        self.future_buckets.clear()
        
        for x in range(self.valid_area[0], self.valid_area[2]):
            for y in range(self.valid_area[1], self.valid_area[3]):
                if Vec(x,y) in self.current:
                    self.current[Vec(x,y)].update(self.current, self.future_buckets)
                    
        self.current.clear()
        
        # Each bucket contains multiple things, so each needs to be collapsed
        # into just one before it is put into the 
        for pos, bucket in self.future_buckets._buckets.iteritems():
            self.current[pos] = bucket.collapse()
                    
                    
    def render(self, renderer):
        for square in self.current:
            renderer.drawAABB(self._get_physics_body(square).hitbox)
        
        
    @property
    def current(self):
        return self._grids[self._current_grid]
    @property
    def future(self):
        return self._grids[(self._current_grid + 1)%2]
    
    # returns the physics body of the block in the grid with location 'pos'
    def _get_physics_body(self, pos):
        ret = PhysicsBody(hitbox=AABB())
        # if pos is not in the grid, it is air
        if pos in self.current:
            ret.hitbox.max = Vec(settings.GRID_SIZE, settings.GRID_SIZE)
            ret.pos = pos*settings.GRID_SIZE
            ret.mass = 1000000
            
        return ret
 
    class FutureBuckets(object):
        def __init__(self, width, height):
            self.width = width;
            self.height = height;
            self._buckets = {}
            # self._buckets_mat = [[Bucket() for i in range(height)] for j in range(width)]
            
        def put(self, pos, thing):
            pos = ImmutableVec.create_dup(pos)
            
            if pos not in self._buckets:
                self._buckets[pos] = Bucket(thing)
            else:
                self._buckets[pos].add(thing)
        
        def clear(self):
            for pos, bucket in self._buckets.iteritems():
                ImmutableVec.done(pos)
            self._buckets.clear()
            
        
