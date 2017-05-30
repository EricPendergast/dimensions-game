import environment

class _State:
    def render(self):
        pass
    def update(self):
        pass
    
class StateFactory:
    @staticmethod
    # creates and returns a new state of the given name
    def init_state(stateNameStr):
        pass
    
    @staticmethod
    def init_state():
        return _GameState()
    
class _GameState(_State):
    def __init__(self):
        self.level = environment.Level()
    
    def render(self):
        self.level.render()
