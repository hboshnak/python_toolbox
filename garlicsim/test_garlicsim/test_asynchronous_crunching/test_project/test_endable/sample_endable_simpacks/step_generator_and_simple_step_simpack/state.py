import garlicsim.data_structures
from garlicsim.misc import WorldEnd

class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    def step_generator(self):
        current_state = self
        while True:    
            if current_state.clock >= 4:
                raise WorldEnd
            old_clock = getattr(current_state, 'clock', 0)
            current_state = State()
            current_state.clock = old_clock + 1
            yield current_state
    
    def step(self):
        if getattr(self, 'clock', 0) >= 4:
            raise WorldEnd
        return State()
            
    @staticmethod
    def create_root():
        return State()
    