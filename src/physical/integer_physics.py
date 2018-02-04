from immutable_vector import ImmutableVec
import copy

class Block(object):
    def __init__(self, grid, pos):
        pos = to_immutable_vec(pos)
        grid[pos] = self
        self.pos = pos
    
    # does not modify grid
    def update(self, grid, future_grid):
        future_grid[self.pos] = self
        # self.vel -= ImmutableVec(0,1)
        
    def render(self, renderer):
        renderer.drawAABB(self._get_physics_body(square).hitbox)
        
        
class GravityBlock(object):
    def __init__(self, grid, pos, vel):
        grid[pos] = self
        self.pos = ImmutableVec.create_dup(pos)
        self.vel = ImmutableVec.create_dup(vel)
    
    # does not modify grid
    def update(self, grid, future_buckets):
        new_self = copy.copy(self)
        for p in get_path(new_self.pos, new_self.pos + new_self.vel):
            future_buckets.put(p, GravityBlock({}, p, ImmutableVec(0,0)))
        
        new_self.pos += self.vel
        new_self.vel -= ImmutableVec(0,1)
        future_buckets.put(new_self.pos, new_self)

# This block indicates whether a spot is occupied at some point between this
# tick and the next
class Path(object):
    pass

class MomentumBlock(object):
    pass

class StationaryBlock(Block):
    pass

# Represents a spot in the grid which can contain more than one block at a
# time. 
class Bucket(object):
    def __init__(self, block):
        self._bucket = {block}
    
    def collapse(self):
        for e in self._bucket:
            return e
    def add(self, block):
        self._bucket.add(block)


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
    

def to_immutable_vec(vec):
    if type(vec) is ImmutableVec:
        return vec
    else:
        return ImmutableVec.create(vec.x, vec.y)
