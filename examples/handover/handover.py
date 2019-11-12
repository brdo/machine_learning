
import math
import random

import numpy as np
from utils import clamp
from vector import Vector
from neural import NeuralNet

WIDTH = 120
HEIGHT = 120

class Beam(object):
    def __init__(self, position, radius, capacity):
        self.position = position
        self.radius = radius
        self.capacity = capacity

        self.reset()

    def reset(self):
        self.load = 0

    def __repr__(self):
        return 'Beam(x=%5.2f, y=%5.2f, r=%5.2f)' % (self.position.x, self.position.y, self.radius)

    def relocate(self):
        pass # self.position = Vector(random.random()*WIDTH, random.random()*HEIGHT)

class Plane(object):
    def __init__(self, position, usage, speed, angle):
        self.position = position
        self.rotation = angle
        self.bearing = Vector(math.cos(self.rotation), math.sin(self.rotation))

        self.neural_net = NeuralNet(5,1,10,1)

        self.usage = usage
        self.speed = speed

        self.reset()

    def reset(self):
        self.fitness = 0
        self.beam = None
        self.th = 0
        self.action = 0

    def update(self, beams):

        beams = sorted([b for b in beams if ((self.beam and b.load < self.beam.load) or self.beam == None) and b != self.beam and b.position.distance(self.position) <= b.radius], key = lambda b: b.load)

        # other beam
        next_beam = beams[0] if beams else None

        if self.beam and abs(self.beam.position.distance(self.position)) >= self.beam.radius:
            self.beam.load -= self.usage*1.0/self.beam.capacity
            self.beam = None
            if next_beam:
                self.th = 0

        sigmoid = lambda x, x0, a, b: a - a/(1 + np.exp(-b*(x-x0)))
        perf = lambda x: np.round(sigmoid(x, 0.9, 1.0, 3.0), 2)

        self.lc = self.beam.load if self.beam else 1

        self.ln = next_beam.load if next_beam else 1

        self.ld = perf(self.ln) - perf(self.lc)

        # current beam
        self.fc = 1 if self.beam else -1

        # next beam
        self.fn = 1 if next_beam else -1

        # time since handover
        if self.beam:
            self.th += 1
        max_th = 10
        self.th = min([self.th, max_th])

        state =  [self.ld, self.fc, self.fn, self.th, self.speed]
        outputs = self.neural_net.update(state)
        self.action = outputs[0]

        if self.action < 0.5:
            # handover
            if self.beam:
                self.beam.load -= self.usage*1.0/self.beam.capacity
                if next_beam:
                    # minimize handovers
                    penalty = 2 * max([0, (max_th - self.th + 1)])
                    if next_beam.load < self.beam.load:
                        penalty *= 0.1
                    self.fitness -= penalty

            self.th = 0
            if next_beam:
                self.beam = next_beam
                self.beam.load += self.usage*1.0/self.beam.capacity
            else:
                if self.beam:
                    self.beam = None
                    self.fitness -= 50
                else:
                    # no current beam
                    pass
        else:
            if self.beam and next_beam:
                if self.beam.load > next_beam:
                    self.fitness -= 0.5 * self.th

        if self.beam:
            fitness = 100 * np.power(perf(self.beam.load), 1)
            self.fitness += fitness

        # calculate new position
        self.position.x += self.bearing.x * self.speed
        self.position.y += self.bearing.y * self.speed

        if self.position.x > WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = WIDTH

        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT

        return self.beam

    def __repr__(self):
        return 'Beam(position=[%s], bearing=[%s], fitness=%s)'\
                % (self.position, self.bearing, self.fitness)

def generate_beams(number):
    beams = []
    s = 30
    for x in range(number):
        for y in range(number):
            position = Vector((x+1)*s, (y+1)*s)
            beam = Beam(position, s*0.866, 100)
            beams.append(beam)

    return beams

def generate_planes_2(number):
    load = 20
    planes = []
    planes.append(Plane(Vector(45, 15), load, 0.1, 0))
    planes.append(Plane(Vector(45, 25), load, 0.1, 0))
    planes.append(Plane(Vector(45, 35), load, 0.1, 0))
    for x in range(number - len(planes)):
        position = Vector(30 + 5*x, 30 + 2*x)
        plane = Plane(position, load, random.random(), random.random()*90)
        # plane = Plane(position, load, 1, random.random()*90)
        planes.append(plane)

    return planes

def generate_planes(number):
    load = 5
    planes = []
    planes.append(Plane(Vector(45, 15), load, 0.0, 0))
    planes.append(Plane(Vector(45, 25), load, 0.0, 0))
    planes.append(Plane(Vector(45, 35), load, 0.0, 0))
    for x in range(number - len(planes)):
        position = Vector(30 + 0.75*x, 10 + 2*x)
        plane = Plane(position, load, 1, 0)
        planes.append(plane)

    return planes
