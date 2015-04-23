
import math
import random

from utils import clamp
from vector import Vector

WIDTH = 100
HEIGHT = 100

class Obstacle(object):
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def edge_distance(self, other):
        return self.position.distance(other.position) - self.radius - other.radius

    def __repr__(self):
        return 'Obstacle(position=[%s], radius=[%s])'\
                % (self.position, self.radius)

class Disk(object):
    def __init__(self):
        self.fitness = 0
        self.chromosome = None
        self.position = Vector(0,0)
        self.radius = 0

    def set_chromosome(self, chromosome):
        self.chromosome = chromosome
        self.position.x = self.chromosome.weights[0] * WIDTH
        self.position.y = self.chromosome.weights[1] * HEIGHT
        self.radius = self.chromosome.weights[2] * 50

    def update(self, obstacles):

        obstacles = sorted(obstacles, key = lambda o: o.edge_distance(self))

        # closest obstacle
        closest_obstacle = obstacles[0]

        edge_distance = closest_obstacle.edge_distance(self)

        if self.position.x - self.radius < 0 or \
           self.position.x + self.radius > WIDTH or \
           self.position.y - self.radius < 0 or \
           self.position.y + self.radius > HEIGHT or \
           edge_distance < 0 or self.radius < 0:
            self.fitness = 0
        else:
            self.fitness = math.pi * math.pow(self.radius, 2)

    def __repr__(self):
        return 'Disk(position=[%s], radius=[%s], fitness=%s)'\
                % (self.position, self.radius, self.fitness)

def generate_obstacles(number):
    obstacles = []
    for _ in range(number):
        position = Vector(random.random() * WIDTH,
                          random.random() * HEIGHT)
        obstacle = Obstacle(position, random.randint(2, 8))
        obstacles.append(obstacle)

    return obstacles

def generate_disks(number):
    disks = []
    for _ in range(number):
        disk = Disk()
        disks.append(disk)

    return disks
