from immutable_vector import ImmutableVec
import copy

class Block(object):
    pass

class StationaryBlock(Block):
    __slots__ = ['pos']
    def __init__(self, pos):
        self.pos = ImmutableVec.create_dup(pos)
    
    # does not modify grid
    def update(self, grid, future_grid):
        future_grid[self.pos] = self
        # self.vel -= ImmutableVec(0,1)
        
    def render(self, renderer):
        renderer.drawAABB(self._get_physics_body(square).hitbox)
        
        
class GravityBlock(Block):
    __slots__ = ['pos', 'vel']
    def __init__(self, pos, vel):
        self.pos = ImmutableVec.create_dup(pos)
        self.vel = ImmutableVec.create_dup(vel)
    
    # does not modify grid
    def update(self, grid, future_buckets):
        new_self = copy.copy(self)
        for p in get_path(new_self.pos, new_self.pos + new_self.vel):
            future_buckets.put(p, GravityBlock(p, ImmutableVec(0,0)))
        
        new_self.pos += self.vel
        new_self.vel -= ImmutableVec(0,1)
        future_buckets.put(new_self.pos, new_self)


def init_in_grid(grid, block):
    grid[int(block.pos.x)][int(block.pos.y)] = block
    return block
    

# Represents a spot in the grid which can contain more than one block at a
# time. 
class BlockBucket(object):
    def __init__(self):
        self._bucket = set()
    
    def collapse(self):
        e = None
        # Returns an arbitrary block from the bucket, None if the bucket is empty
        for e in self._bucket:
            break
        return e
        
    def add(self, block):
        self._bucket.add(block)
    
    def clear(self):
        self._bucket.clear()


def get_path(a, b):
    assert type(a) is ImmutableVec
    assert type(b) is ImmutableVec
    assert b.copy().round() == b
    assert a.copy().round() == a
    
    if b == a:
        return {a.copy()}
    
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
    
