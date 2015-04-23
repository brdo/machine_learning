
import math
from numpy import linalg

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt(math.pow(other.x - self.x,2) + math.pow(other.y - self.y,2))

    def __len__(self):
        return linalg.norm([self.x, self.y])

    def normalize(self):
        length = linalg.norm([self.x, self.y])
        self.x /= length
        self.y /= length

    def __str__(self):
        return 'x=%5.2f, y=%5.2f' % (self.x, self.y)

