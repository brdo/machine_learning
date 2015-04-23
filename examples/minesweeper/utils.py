
import random

def random_clamped():
    """
    generate a random number from -1 to 1
    """
    return random.random() - random.random()


def clamp(val, lower, upper):
    """
    return the value clamped by the lower and upper bounds
    """
    if val < lower:
        return lower
    elif val > upper:
        return upper
    else:
        return val

