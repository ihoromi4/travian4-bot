import time
import random

from . import statemachine


class FarmVillage(statemachine.StateMachine):
    def __init__(self, village, pos):
        statemachine.StateMachine.__init__(self)
        self.village = village
        self.pos = pos
        self.attack_period = 7 * 60 + 180 * random.random()
        self.last_attack_time = 0
        self.set_state(self.state_wait)

    def state_wait(self):
        if time.time() - self.last_attack_time > self.attack_period:
            self.set_state(self.state_raid)

    def state_raid(self):
        self.last_attack_time = time.time()
        self.village.troops.attack_raid(self.pos)
        self.set_state(self.state_wait)
