class Vec(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def dot(self, vec):
        return self.x*vec.x + self.y*vec.y
    
    def copy(self):
        return Vec(self.x, self.y)
    # def mag(self):
        # return sqrt(
    def magSquared(self):
        return self.x*self.x + self.y*self.y
    
    def __add__(self, vec):
        return Vec(self.x + vec.x, self.y + vec.y)
    
    def __sub__(self, vec):
        return Vec(self.x - vec.x, self.y - vec.y)
    
    def __mul__(self, val):
        return Vec(self.x*val, self.y*val)
    
    def __div__(self, val):
        return Vec(self.x/val, self.y/val)
    
    def __str__(self):
        return str((self.x,self.y))



# Contains all the information required to resolve a  collision
class Manifold(object):
    def __init__(self, depth=0, normal=None, contact=None):
        self.depth = depth
        self.normal = Vec(0,1) if normal is None else normal
        self.contact = Vec(0,0) if contact is None else contact
        

# the AABB(Axis Aligned Bounding Box), is defined where 'min' is the lower left
# point, and 'max' is the upper right point
class AABB(object):
    def __init__(self, min=None, max=None):
        self.min = Vec(0,0) if min is None else min
        self.max = Vec(0,0) if max is None else max
    
    def is_valid(self):
        return self.min.x <= self.max.x and self.min.y <= self.max.y
    
    def intersect(self, other):
        return self.get_intersection_box(other).is_valid()
    
    def get_intersection_box(self, other):
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
    def __init__(self, pos=None, vel=None, acc=None, hitbox=None, mass=50, restitution = 1):
        # self.hitbox = Square(Vec(0,0), 30)
        self.hitbox = AABB(Vec(0,0), Vec(30,30)) if hitbox is None else hitbox
        self.pos = Vec() if pos is None else pos
        self.vel = Vec() if vel is None else vel
        self.acc = Vec() if acc is None else acc
        self.mass = mass
        self.restitution = restitution
    
    def update(self):
        # print("PLAYER" + str(self.vel))
        # apply acceleration
        # self.vx += self.ax
        # self.vy += self.ay
        self.vel += self.acc
        # apply velocity
        # self.x += self.vx
        # self.y += self.vy
        # self.pos = self.pos + self.vel
        self.pos += self.vel
    
    def intersect(self, body):
        return self.hitbox.intersect(body.hitbox)
        
    @property
    def pos(self):
        return self.hitbox.pos
    
    @pos.setter
    def pos(self, pos):
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
    def __init__(self, gravity=Vec(0,-.01)):
        self.gravity = gravity
    
    # Enacts gravity, air resistance
    def enact_single(self, body):
        # body.vel += self.gravity
        body.update()
        body.vel *= .95
    
    def enact_pair(self, bodyA, bodyB):
        manifold = bodyA.get_manifold(bodyB)
        
        if manifold.depth <= 0:
            if bodyA.intersect(bodyB):
                print "Something bad"
            return
        
        print("Intersecting")
        
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
        
        # Penetration correction
        # Penetration allowed before penetration correction starts
        k_slop = .01
        # Fraction of the penetration that is resolved each iteration
        percent = .2
        
        correction = manifold.normal * -percent * (max(manifold.depth - k_slop, 0)/(1.0/bodyA.mass + 1.0/bodyB.mass))
        
        bodyA.pos -= correction / bodyA.mass
        bodyB.pos += correction / bodyB.mass
        
    def enact_group(self, bodies=[]):
        if bodies[0].intersect(bodies[1]):
            print("Intersecting")
        

# class Rectangle(object):
#     def __init__(self, vec=Vec(), width=0, height=0):
#         self.pos = vec
#         self.width = width
#         self.height = height
#
#     def intersect(self, other):
#         return self._intervalIntersect(self.pos.x, self.pos.x + self.width, other.pos.x, other.pos.x + other.width) and\
#                 self._intervalIntersect(self.pos.y, self.pos.y + self.height, other.pos.y, other.pos.y + other.height)
#
#     def get_manifold(self, other):
#         pass
#         # depth =
#     # Precondition: a<b, c<d
#     # (a,b) is the first interval, (c,d) is the second
#     def _intervalIntersect(self, a, b, c, d):
#         # print((a,b,c,d))
#         return abs(c+d-a-b) < b+d-a-c
#
# class Square(Rectangle):
#     def __init__(self, vec=Vec(), size=0):
#         Rectangle.__init__(self, vec, size, size)
#
