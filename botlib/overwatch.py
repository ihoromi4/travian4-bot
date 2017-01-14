import time

from guilib import push


class Overwatch:
    def __init__(self, account):
        self.account = account
        self.push_bullet = None
        self.attacks = dict()

    def on_attack(self):
        pass

    def add_pushbullet(self, api_key):
        push.init(api_key)
        self.push_bullet = True

    def inspect(self):
        for village in self.account.villages:
            movements = village.troops.get_movements()
            if 'in-attack' in movements:
                in_attack = movements['in-attack']
                number = in_attack['number']
                if self.attacks.get(village.id, 0) < number:
                    if self.push_bullet:
                        push.send('Incoming attack!', 'Begin attack on village: {}'.format(village.name))
                    self.on_attack()
                    self.attacks[village.id] = number
            else:
                self.attacks[village.id] = 0
