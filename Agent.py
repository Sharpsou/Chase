from random import *
from pandas import DataFrame

class Agent:
    def __init__(self, x, y, grid, detection_range):
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
        self.memory = []
        self.radar = []
        self.radar_agent = []
        self.grid = grid
        self.agents = []

    def next_mouvement(self, protocol):
        self.get_radar()
        self.next_direction()
        x = self.position_x + self.direction_x
        y = self.position_y + self.direction_y
        if protocol.possibles_movements(x, y):
            self.temp_position_x = x
            self.temp_position_y = y
            self.reward = 1
        else:
            self.reward = -1

    def next_direction(self):
        self.direction_x = randint(-1, 1)
        self.direction_y = randint(-1, 1)

    def get_radar(self):
        self.radar = []
        self.radar_agent = [[0 for m in range((self.detection_range*2)+1)] for n in range((self.detection_range*2)+1)]

        for i in range((self.detection_range*2)+1):
            i -= self.detection_range
            line = []
            for j in range((self.detection_range*2)+1):
                j -= self.detection_range
                out = False
                x = self.position_x + i
                y = self.position_y + j
                if x < 0 : 
                    x = 0
                    out = True

                if x > self.grid.width-1 : 
                    x = self.grid.width-1
                    out = True
                if y < 0 : 
                    y = 0
                    out = True
                if y > self.grid.height-1 : 
                    y = self.grid.height-1
                    out = True

                value = self.grid.map[y][x]
                if out : value = 1
                line.append(value)
                
                for agent in self.agents:
                    if agent.position_x == x and agent.position_y == y and not out:
                        if type(agent) == type(self):
                            if agent != self:self.radar_agent[i+self.detection_range][j+self.detection_range] = 1
                        else:
                            self.radar_agent[i+self.detection_range][j+self.detection_range] = -1

            self.radar.append(line)


class Hunter(Agent):
    def __init__(self, x, y, grid, detection_range):
        super().__init__(x, y, grid, detection_range)
        self.health = 1
        self.detection_range = detection_range
        self.resolution = 2 # self.detection_range  # self.detection_range-1 if self.detection_range > 1 else 1
        #self.get_radar(env)
        #self.brain = Brain(name='Hunter', agent=self)


class Prey(Agent):
    def __init__(self, x, y, grid, detection_range):
        super().__init__(x, y, grid, detection_range)
        self.health = 2
        self.detection_range = detection_range
        self.resolution = 2 # self.detection_range  # self.detection_range-1 if self.detection_range > 1 else 1
        #self.get_radar(env)
        #self.brain = Brain(name='Prey', agent=self)