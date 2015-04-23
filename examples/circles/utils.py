
import random

def random_clamped():
    return random.random() - random.random()

def clamp(val, lower, upper):
    if val < lower:
        return lower
    elif val > upper:
        return upper
    else:
        return val

