import physics

class SimpleEntity:
    def __init__(self, body=None):
        self.body = physics.PhysicsBody() if body is None else body
    
    def render(self, renderer):
        renderer.drawAABB(self.body.hitbox)
