

class StateMachine:
    def __init__(self):
        self.active_state = None
        self.transitions = {}

    def set_state(self, state):
        self.active_state = state

    def add_transition(self, state, condition, new_state):
        transitions = self.transitions.get(state, [])
        transitions.append((condition, new_state))
        self.transitions[state] = transitions

    def update(self):
        if self.active_state:
            transitions = self.transitions.get(self.active_state, [])
            self.active_state()
            for condition, new_state in transitions:
                if condition():
                    self.active_state = new_state
                    break
