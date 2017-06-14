class Vec(object):
    def __init__(self, x=0, y=0, str=None):
        if not str is None:
            splitted = str.split(",")
            self.x = float(splitted[0])
            self.y = float(splitted[1])
        else:
            self.x = float(x)
            self.y = float(y)
        
        assert type(self.x) is float
        assert type(self.y) is float
        
    def dot(self, vec):
        assert type(vec) is Vec
        return self.x*vec.x + self.y*vec.y
    
    def copy(self):
        return Vec(self.x, self.y)
    # def mag(self):
        # return sqrt(
    def magSquared(self):
        return self.x*self.x + self.y*self.y
    
    def __add__(self, vec):
        assert type(vec) is Vec
        return Vec(self.x + vec.x, self.y + vec.y)
    
    def __sub__(self, vec):
        assert type(vec) is Vec
        return Vec(self.x - vec.x, self.y - vec.y)
    
    def __mul__(self, val):
        return Vec(self.x*val, self.y*val)
    
    def __div__(self, val):
        return Vec(self.x/val, self.y/val)
    
    def __str__(self):
        return str((self.x,self.y))

    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y

    def __hash__(self):
        return hash((self.x,self.y))

# Contains all the information required to resolve a  collision
class Manifold(object):
    def __init__(self, depth=0, normal=None, contact=None):
        self.depth = float(depth)
        self.normal = Vec(0,1) if normal is None else normal
        self.contact = Vec(0,0) if contact is None else contact
        
        assert type(self.depth) is float
        assert type(self.normal) is Vec
        assert type(self.contact) is Vec
        

# the AABB(Axis Aligned Bounding Box), is defined where 'min' is the lower left
# point, and 'max' is the upper right point
class AABB(object):
    def __init__(self, min=None, max=None):
        self.min = Vec(0,0) if min is None else min
        self.max = Vec(0,0) if max is None else max
        
        assert type(self.min) is Vec
        assert type(self.max) is Vec
    
    def is_valid(self):
        return self.min.x <= self.max.x and self.min.y <= self.max.y
    
    def intersect(self, other):
        assert type(other) is AABB
        return self.get_intersection_box(other).is_valid()
    
    def get_intersection_box(self, other):
        assert type(other) is AABB
        return AABB(
                Vec(max(self.min.x, other.min.x), max(self.min.y, other.min.y)),
                Vec(min(self.max.x, other.max.x), min(self.max.y, other.max.y)))
    
    # 'a' is self
    def get_manifold(a, b):
        assert type(b) is AABB
        
        manifold = Manifold()
        aToB = b.min - a.min
        
        if aToB.magSquared() == 0:
            manifold.depth = a.width
            manifold.normal = Vec(-1,0)
            manifold.contact = a.pos.copy()
            return manifold
        
        intersect = a.get_intersection_box(b)
        
        if not intersect.is_valid():
            return manifold
        
        if intersect.width < intersect.height:
            manifold.normal = Vec(1,0) if aToB.x < 0 else Vec(-1,0)
            manifold.depth = intersect.width
        else:
            manifold.normal = Vec(0,1) if aToB.y < 0 else Vec(0,-1)
            manifold.depth = intersect.height
            
        
        return manifold
        
    @property
    def pos(self):
        return self.min
    
    @pos.setter
    def pos(self, pos):
        translate = pos - self.min
        self.min += translate
        self.max += translate
        
    @property
    def width(self):
        return self.max.x - self.min.x
    
    @property
    def height(self):
        return self.max.y - self.min.y
    
    def __str__(self):
        return "AABB" + str(self.min) + str(self.max)
    
    


class PhysicsBody(object):
    def __init__(self, pos=None, vel=None, acc=None, hitbox=None, mass=50, restitution = 0, mu = 9):
        # self.hitbox = Square(Vec(0,0), 30)
        self.hitbox = AABB(Vec(0,0), Vec(30,40)) if hitbox is None else hitbox
        self.pos = Vec() if pos is None else pos
        self.vel = Vec() if vel is None else vel
        self.acc = Vec() if acc is None else acc
        self.mass = mass
        self.restitution = restitution
        self.mu = mu
    
    def update(self):
        # apply acceleration
        self.vel += self.acc
        # apply velocity
        self.pos += self.vel
    
    def intersect(self, body):
        return self.hitbox.intersect(body.hitbox)
        
    @property
    def pos(self):
        return self.hitbox.pos
    
    @pos.setter
    def pos(self, pos):
        assert type(pos) is Vec
        self.hitbox.pos = pos
        
    def get_manifold(self, other):
        return self.hitbox.get_manifold(other.hitbox)
    # @property
    # def width(self):
    #     return self.hitbox.width
    # # @width.setter
    # # def width(self, width):
    # #     self.hitbox.width = width
    #
    # @property
    # def height(self):
    #     return self.hitbox.height
    # # @height.setter
    # # def height(self, height):
    # #     self.hitbox.height = height
    #
        

class PhysicsEnacter(object):
    # self.gravity is the acceleration due to gravity
    def __init__(self, gravity=Vec(0,-.3)):
        self.gravity = gravity
    
    # Enacts gravity, air resistance
    def enact_single(self, body):
        body.vel += self.gravity
        body.update()
        # body.vel *= .95
    
    def enact_pair(self, bodyA, bodyB):
        manifold = bodyA.get_manifold(bodyB)
        
        if manifold.depth <= 0:
            # if bodyA.intersect(bodyB):
                # print "Something bad"
            return
        
        # print("Intersecting")
        
        # relative velocity of 'bodyA' and 'bodyB'
        rv = bodyB.vel - bodyA.vel
        contactVel = rv.dot(manifold.normal)
        
        if contactVel < 0:
            return
        
        # restitution
        e = min(bodyA.restitution, bodyB.restitution)
        # impulse magnitude
        j = -(1.0 + e) * contactVel
        j /= 1.0/bodyA.mass + 1.0/bodyB.mass
        
        impulse = manifold.normal * j 
        
        bodyA.vel -= impulse/bodyA.mass
        bodyB.vel += impulse/bodyB.mass
        
        # 'impulse' is also the normal force. We can use this to derive the
        # force of friction.
        frictionDir = rv - manifold.normal*rv.dot(manifold.normal)
        # friction = (impulse - (manifold.normal * impulse.dot(manifold.normal))) * min(bodyA.mu,  bodyB.mu)
        friction = frictionDir * min(bodyA.mu,  bodyB.mu)
        
        bodyA.vel += friction/bodyA.mass
        bodyB.vel -= friction/bodyB.mass
        # Penetration correction
        # Penetration allowed before penetration correction starts
        k_slop = .01
        
        # Fraction of the penetration that is resolved each iteration
        percent = .8
        correction = manifold.normal * -percent * (max(manifold.depth - k_slop, 0)/(1.0/bodyA.mass + 1.0/bodyB.mass))
        
        bodyA.pos -= correction / bodyA.mass
        bodyB.pos += correction / bodyB.mass
        
    # def enact_group(self, bodies=[]):
    #     if bodies[0].intersect(bodies[1]):
    #         print("Intersecting")
