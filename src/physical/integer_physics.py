from immutable_vector import ImmutableVec
from physics import Vec
import copy

class Block(object):
    def __init__(self, BlockType, pos, *args, **kwargs):
        self.pos = ImmutableVec.create_dup(pos)
        self.init(BlockType, *args, **kwargs)
    
    def init(self, BlockType, *args, **kwargs):
        assert issubclass(BlockType, BlockShell)
        self.BlockType = BlockType
        self.BlockType.init(self, *args, **kwargs)
        
    def update(self, grid, future_grid):
        self.BlockType.update(self, grid, future_grid)
        
    def collapse(self, into):
        self.BlockType.collapse(self, into)
        
    def __repr__(self):
        return self.BlockType.to_string(self)
    

# Subclasses of BlockShell are just "shells" around blocks which define their
# behavior. It is designed this way so that each block can occupy only one
# spot, and when a block moves, we don't need to initialize a new block. Notice
# that the static methods have a 'self' field, which doesn't refer to an
# instance of BlockShell, but to an instance of Block.
class BlockShell(object):
    def __new__(cls):
        raise NotImplementedError()
    
    @staticmethod
    def init(self):
        pass
    
    @staticmethod
    def update(self, grid, future_grid):
        pass
    
    @staticmethod
    def collapse(self, into):
        pass
    
    @staticmethod
    def to_string(self):
        return self.BlockType.__name__ + "(" + str(self.pos.x) + ", " + str(self.pos.y) + ")"

class Air(BlockShell):
    pass

# This serves as a container for the behavior (not data) of a stationary block.
# It should never be initialized
# class StationaryBlock(BlockShell):
#     @staticmethod
#     def init(self, pos):
#         obj.pos = pos
#
#     # does not modify grid
#     @staticmethod
#     def update(self, grid, future_grid):
#         future_grid[self.pos] = self
#         # self.vel -= ImmutableVec(0,1)
#
        
        
class GravityBlock(BlockShell):
    
    @staticmethod
    def init(self, vel):
        self.vel = ImmutableVec.create_dup(vel)
    
    @staticmethod
    def update(self, grid, future_buckets):
        for p in get_path(self.pos, self.pos + self.vel):
            future_buckets.put(p, GravityBlock, ImmutableVec(0,0))
        future_buckets.put(self.pos + self.vel, GravityBlock, self.vel - ImmutableVec(0,1))
        
        print future_buckets
        
    @staticmethod
    def collapse(self, into):
        into.init(self.BlockType, vel=self.vel)
    
    @staticmethod
    def to_string(self):
        return self.BlockType.__name__ + "(" + str(self.pos.x) + ", " + str(self.pos.y) + ")(" + str(self.vel.x) + ", " + str(self.vel.y) + ")"

def init_in_grid(grid, pos, BlockType, *args, **kwargs):
    grid[int(pos.x)][int(pos.y)].init(BlockType, *args, **kwargs)


# Represents a spot in the grid which can contain more than one block at a
# time. 
class BlockBucket(object):
    def __init__(self, pos):
        self.pos = ImmutableVec.create_dup(pos)
        self._bucket = []
        self._reserve = []
    
    def collapse(self, into):
        e = None
        # Returns an arbitrary block from the bucket, None if the bucket is
        # empty
        for e in self._bucket:
            if type(e) is not Air:
                break
        if e is None:
            into.init(Air)
        else:
            e.collapse(into)
        
    def put(self, BlockType, *args, **kwargs):
        if not self._reserve:
            self._bucket.append(Block(BlockType, self.pos, *args, **kwargs))
        else:
            to_append = self._reserve.pop()
            to_append.init(BlockType, *args, **kwargs)
            self._bucket.append(to_append)
        
    def clear(self):
        while self._bucket:
            self._reserve.append(self._bucket.pop())
            
    def __repr__(self):
        return "(" + str(self.pos) + ": " + str(self._bucket) + ")"


def get_path(a, b):
    a = ImmutableVec.create_dup(a)
    b = ImmutableVec.create_dup(b)
    assert b.copy().round() == b
    assert a.copy().round() == a
    
    if b == a:
        return set()
    
    path = set()
    
    direction = (b-a).normalize()/3
    
    # TODO: Make this less shoddy. Possible risk of infinite loop.
    pos = a
    while b not in path:
        # print path
        path.add(pos.copy().round())
        pos += direction
        
    path.remove(b)
    
    return path

