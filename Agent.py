from random import *


class Agent:
    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y
        self.temp_position_x = x
        self.temp_position_y = y
        self.direction_x = randint(-1, 1)
        self.direction_y = randint(-1, 1)
        self.detection_range = 0
        self.resolution = 0
        self.dol = 8
        self.reward = 0
        self.done = False
        self.history_acc = []


class Hunter(Agent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 1
        self.detection_range = 4
        self.resolution = 2 # self.detection_range  # self.detection_range-1 if self.detection_range > 1 else 1
        #self.get_radar(env)
        #self.brain = Brain(name='Hunter', agent=self)


class Prey(Agent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 2
        self.detection_range = 4
        self.resolution = 2 # self.detection_range  # self.detection_range-1 if self.detection_range > 1 else 1
        #self.get_radar(env)
        #self.brain = Brain(name='Prey', agent=self)