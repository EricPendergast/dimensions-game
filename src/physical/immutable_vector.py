from Queue import Queue
import sys
import math


class ImmutableVec(object):
    __slots__ = ['x','y']
    pool = Queue(maxsize=0)
        
    # Making this class immutable
    def __setattr__(self, *args):
        raise TypeError
    def __delattr__(self, *args):
        raise TypeError
    
    @classmethod
    def create(cls, x, y):
        assert type(x) is float
        assert type(y) is float
        
        return ImmutableVec(x,y)
    
        if cls.pool.empty():
            return ImmutableVec(x,y)
        else:
            vec = cls.pool.get()
            # Changing an "immutable" object
            object.__setattr__(vec, "x", float(x))
            object.__setattr__(vec, "y", float(y))
            return vec
    
    # Creates a duplicate of 'vec', as an ImmutableVec
    @classmethod
    def create_dup(cls, vec):
        # Since it is immutable, we can share references without problems
        if type(vec) is ImmutableVec:
            return vec
        else:
            return ImmutableVec.create(vec.x, vec.y)
        
    @classmethod
    def done(cls, vec):
        # assert sys.getrefcount(object) == 1
        assert type(vec) is ImmutableVec
        cls.pool.put(vec)
        
    @classmethod
    def init_from_string(cls, str):
        splitted = str.split(",")
        x = float(splitted[0])
        y = float(splitted[1])
        vec = ImmutableVec.create(x,y)
        return vec
    
    @classmethod
    def init_from_tupple(cls, tupple):
        x = tupple[0]
        y = tupple[1]
        vec = ImmutableVec.create(x,y)
        return vec
        
    def __init__(self, x=0, y=0):
        object.__setattr__(self, "x", float(x))
        object.__setattr__(self, "y", float(y))
        
        assert type(self.x) is float
        assert type(self.y) is float
        
    def dot(self, vec):
        return self.x*vec.x + self.y*vec.y
    
    def copy(self):
        return ImmutableVec.create(self.x, self.y)
    
    def magSquared(self):
        return self.x*self.x + self.y*self.y
    
    def round(self):
        return ImmutableVec.create(round(self.x), round(self.y))
    
    def normalize(self):
        mag = math.sqrt(self.magSquared())
        return self / mag
    
    def __add__(self, vec):
        return ImmutableVec.create(self.x + vec.x, self.y + vec.y)
    
    def __sub__(self, vec):
        return ImmutableVec.create(self.x - vec.x, self.y - vec.y)
    
    def __mul__(self, val):
        return ImmutableVec.create(self.x*val, self.y*val)
    
    def __div__(self, val):
        return ImmutableVec.create(self.x/val, self.y/val)
    
    def __str__(self):
        return str((self.x,self.y))
    
    def __repr__(self):
        return str(self)
    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y

    def __hash__(self):
        return hash((self.x,self.y))
