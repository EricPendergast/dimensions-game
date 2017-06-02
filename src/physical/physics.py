class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def intersect(self, other_rectangle):
        pass

class Square:
    def __init__(self, x=0, y=0, size=0):
        self.x = x
        self.y = y
        self.size = size
    
    def intersect(self, other_square):
        dx = abs(self.x - other_square.x)
        dy = abs(self.y - other_square.y)
        
        return (dx < self.size/2 | dy < self.size/2)
        

class PhysicsBody:
    def __init__(self, x=0, y=0, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        
        self.hitbox = Square(x, y, 30)
    
    def update(self):
        # apply acceleration
        self.vx += self.ax
        self.vy += self.ay
        # apply velocity
        self.x += self.vx
        self.y += self.vy
        
    @property
    def x(self):
        return hitbox.x
    @x.setter
    def x(self, x):
        self.hitbox.x = x
    
    @property
    def y(self):
        return hitbox.y
    @y.setter
    def y(self, y):
        self.hitbox.y = y
        
    @property
    def width(self):
        return self.hitbox.size
    @width.setter
    def width(self, width):
        self.hitbox.width = size
    
    @property
    def height(self):
        return self.hitbox.size
    @height.setter
    def height(self, height):
        self.hitbox.height = size
