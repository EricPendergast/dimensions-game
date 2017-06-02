import player
import settings
import json

class Level:
    def __init__(self):
        # grid contains all the blocks in the current level. If a coordinate is
        # not one of the keys in grid, it is assumed to be air
        self.grid = {}
        self.load("1.lvl")
        self.player = player.Player()
        # self.save("1.lvl")
    
    def render(self, renderer):
        for square in self.grid.keys():
            point = [int(i)*settings.GRID_SIZE for i in square.split(",")]
            renderer.drawRect(*(point + [settings.GRID_SIZE]*2))
        
        self.player.render(renderer)
    
    def update(self, inputHandler):
        self.player.update(inputHandler)
        
    def save(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "w")
        file.write(json.dumps(self.grid))
        
    def load(self, filename):
        file = open(settings.LEVEL_SAVES_PATH + filename, "r")
        self.grid = json.loads(file.read())
        
