from enum import Enum
import math
    
    
class Color(Enum):
    white = 1
    red = 2
    blue = 3
    purple = 4
    green = 5
    yellow = 6
    
    
class Direction(Enum):
    left = 1
    right = 2
    up = 3
    down = 4
    
   
class Orientation(Enum):
    vertical = 1
    horizontal = 2
    
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def to_tuple(self):
        return (self.x, self.y)
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)
        
    
class Match:
     def __init__(self, point, color, orientation, length, points, chain_level = 1):
         self.point = point
         self.color = color.name if color != None else "unknown"
         self.orientation = orientation
         self.length = length
         self.points = self._get_points(points, chain_level)
         self.chain_level = chain_level
         
     def update_chain_level(self, chain_level):
         self.chain_level = chain_level
         self.points = self._get_points(self.points, chain_level)

     def _get_points(self, points, chain_level):
        return points * math.pow(2, chain_level - 1)        # Chain multiplier is set to 2, modify if needed (to avoid circular dependencies)
         
     def __str__(self):
         return "%s %s %s x%d -- %d points, chain #%d" % (self.color, self.point, self.orientation.name, self.length, self.points, self.chain_level)