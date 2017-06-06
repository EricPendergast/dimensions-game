import player
import physics

import settings
# import json
import pickle as json

class Level:
    def __init__(self):
        # grid contains all the blocks in the current level. If a coordinate is
        # not one of the keys in grid, it is assumed to be air
        self.grid = {}
        self.grid["5,5"] = 1
        self.grid["5,6"] = 1
        self.grid["5,7"] = 1
        self.grid["5,8"] = 1
        self.grid["5,9"] = 1
        self.load("1.lvl")
        
        self.player = player.Player(physics.Vec(40,40), mass=5000)
        self.body1 = physics.PhysicsBody(physics.Vec(200,200))
        
        print("PLAYER" + str(id(self.player.body.vel)))
        print(id(self.body1.vel))
        # print("PLAYER" + str(self.player.body.pos))
        # print(self.body1.pos)
        self.physics = physics.PhysicsEnacter()
        # self.save("1.lvl")
    
    def render(self, renderer):
        for square in self.grid.keys():
            point = [int(i)*settings.GRID_SIZE for i in square.split(",")]
            renderer.drawRect(*(point + [settings.GRID_SIZE]*2))
        
        self.player.render(renderer)
        renderer.drawAABB(self.body1.hitbox)
    
    def update(self, inputHandler):
        self.player.update(inputHandler)
        
        self.physics.enact_single(self.player.body)
        self.physics.enact_single(self.body1)
        # self.physics.enact_group([self.player.body, physics.PhysicsBody(physics.Vec(0,0))])
        self.physics.enact_pair(self.player.body, self.body1)
        
        # At some point, I will have a list of entities, and I will call 
        
    def save(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "w")
        file.write(json.dumps(self.grid))
        
    def load(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "r")
        self.grid = json.loads(file.read())
        
