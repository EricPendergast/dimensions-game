import state

class StateManager:
    
    def __init__(self):
        self.states = {"main": None, "game":state.StateFactory.init_state()}
        self.currentState = "game"
        
    def update(self):
        none
        
    def render(self, renderer):
        self.states[self.currentState].render(renderer)
        
