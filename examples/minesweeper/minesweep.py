#!/usr/bin/python

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

        self.neural_net = NeuralNet(4,1,6,2)
        self.fitness = 0

    def update(self, mines):

        mine = sorted(mines, key = lambda m: m.position.distance(self.position))[0]
        vec = Vector(mine.position.x, mine.position.y)
        vec.normalize()

        outputs = self.neural_net.update([vec.x, vec.y,
                                          self.bearing.x, self.bearing.y])


        self.speed = outputs[0] + outputs[1]
        self.rotation += clamp(outputs[0] - outputs[1], -0.3, 0.3)

        self.bearing.x = -math.sin(self.rotation)
        self.bearing.y = math.cos(self.rotation)
        self.bearing.normalize()

        self.position.x += self.bearing.x * self.speed
        self.position.y += self.bearing.y * self.speed

        if self.position.x > WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT

        return mine

    def __repr__(self):
        return 'Tank(position=[%s], bearing=[%s], fitness=%s)' % (self.position, self.bearing, self.fitness)

def generate_mines(number):
    mines = []
    for _ in range(number):
        position = Vector(random.random()*WIDTH, random.random()*HEIGHT)
        mine = Mine(position)
        mines.append(mine)

    return mines

def generate_tanks(number):
    tanks = []
    for _ in range(number):
        position = Vector(random.random()*WIDTH, random.random()*HEIGHT)
        tank = Tank(position)
        tanks.append(tank)

    return tanks
