
import math
import random

from utils import clamp
from vector import Vector
from neural import NeuralNet

WIDTH = 100
HEIGHT = 100

class Mine(object):
    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return 'Mine(x=%5.2f, y=%5.2f)' % (self.position.x, self.position.y)

    def relocate(self):
        self.position = Vector(random.random()*WIDTH, random.random()*HEIGHT)

class Tank(object):
    def __init__(self, position):
        self.position = position
        self.rotation = random.random() * 2 * math.pi
        self.bearing = Vector(math.cos(self.rotation), math.sin(self.rotation))

        self.neural_net = NeuralNet(4,1,6,3)
        self.fitness = 0

    def update(self, mines):

        mines = sorted(mines, key = lambda m: m.position.distance(self.position))

        # closest mine
        closest_mine = mines[0]

        # look_at vector
        look_at = Vector(self.position.x - closest_mine.position.x,
                         self.position.y - closest_mine.position.y)
        look_at.normalize()

        outputs = self.neural_net.update([look_at.x, look_at.y,
                                          self.bearing.x, self.bearing.y])

        # rotation
        self.rotation += (outputs[0] - outputs[1]) * 0.01

        # speed
        self.speed = outputs[2]

        # calcuate new bearing
        degrees = self.rotation * 180 / math.pi
        self.bearing.x = -math.sin(degrees)
        self.bearing.y = math.cos(degrees)

        # calculate new position
        self.position.x += self.bearing.x * self.speed
        self.position.y += self.bearing.y * self.speed

        self.position.x = clamp(self.position.x, 0, WIDTH)
        self.position.y = clamp(self.position.y, 0, HEIGHT)

        return closest_mine

    def __repr__(self):
        return 'Tank(position=[%s], bearing=[%s], fitness=%s)'\
                % (self.position, self.bearing, self.fitness)

def generate_mines(number):
    mines = []
    for _ in range(number):
        position = Vector(random.random() * WIDTH,
                          random.random() * HEIGHT)
        mine = Mine(position)
        mines.append(mine)

    return mines

def generate_tanks(number):
    tanks = []
    for _ in range(number):
        position = Vector(random.random() * WIDTH,
                          random.random() * HEIGHT)
        tank = Tank(position)
        tanks.append(tank)

    return tanks
