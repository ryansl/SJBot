from enum import Enum
import math
    
    
class Color(Enum):
    white = "WHITE"
    red = "RED"
    blue = "BLUE"
    purple = "PURPLE"
    green = "GREEN"
    yellow = "YELLOW"
    
    
class Direction(Enum):
    left = "LEFT"
    right = "RIGHT"
    up = "UP"
    down = "DOWN"
    
   
class Orientation(Enum):
    vertical = "VERTICAL"
    horizontal = "HORIZONTAL"
    
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def to_tuple(self):
        return (self.x, self.y)
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    
class Match:
     def __init__(self, point, color, orientation, length, points, chain_level = 1):
         self.point = point
         self.color = color
         self.orientation = orientation
         self.length = length
         self.points = points
         self.chain_level = chain_level
         
     def update_chain_level(self, chain_level):
         self.chain_level = chain_level
         self.points = self._get_points(self.points, chain_level)
         
     def _get_points(self, base_points, chain_level):
        return base_points * pow(2, chain_level - 1)