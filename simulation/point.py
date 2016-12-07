from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
        
from math import sqrt
def dist(a, b):
    return sqrt( (a.x - b.x)**2 + (a.y - b.y)**2 )
