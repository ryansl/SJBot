from enum import Enum
    
    
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
        
    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)
        
    
class Match:
     def __init__(self, point, orientation, length):
         self.point = point
         self.orientation = orientation
         self.length = length
         self.points = Configuration.points_table[length]
         
     def __str__(self):
         return "%s %s x%d -- %d points" % (self.point, self.orientation.name, self.length, self.points)