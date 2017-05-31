import settings
class Level:
    def __init__(self):
        self.grid = {}
        self.grid[(5,5)] = "a"
        self.grid[(6,5)] = "a"
        self.grid[(7,5)] = "a"
        self.grid[(8,5)] = "a"
        self.grid[(9,5)] = "a"
    
    def render(self, renderer):
        print("Rendering")
        
        # renderer.drawRect(60,60,100,5000)
        
        for square in self.grid.keys():
            point = [i*settings.GRID_SIZE for i in square]
            renderer.drawRect(*(point + [settings.GRID_SIZE]*2))
        
        
