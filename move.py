from definitions import *
from configuration import *
from board import *
import autopy
import math
import time


class Move:
    def __init__(self, point, direction, delay = 0):
        self.point = point
        self.direction = direction
        self.delay = delay if delay > 0 else 0
    
    
    # Make the move by moving the mouse to the specific coordinates
    def make(self):
        if not valid_point(self.point):
            return False
            
        # Original X and Y coordinates
        x = self.point.x
        y = self.point.y
        
        
        # Compute the coordinates of the starting and ending clicks
        ox = Configuration.offset_x
        oy = Configuration.offset_y
        gr = Configuration.grid_size
        gs = Configuration.gem_size
        
        x = int(math.floor(ox + ((self.point.x - 1) * gs) + (gs / 2)))
        y = int(math.floor(oy + ((self.point.y - 1) * gs) + (gs / 2)))
        dx = 0
        dy = 0
        tx = 0
        ty = 0
    
        if self.direction == Direction.up:       dy = -1
        elif self.direction == Direction.down:   dy = 1
        elif self.direction == Direction.left:   dx = -1
        elif self.direction == Direction.right:  dx = 1000
    
        tx = x + (dx * gs)
        ty = y + (dy * gs)
    
    
        # If the starting or ending mouse position is not in the grid, then don't try to move
        # NOTE: Exceptions are really expensive! They cost about 100ms of time
        if x < ox or y < oy or tx < ox or ty < oy or x > ox + gr or y > oy + gr or tx > ox + gr or ty > oy + gr:
            return
    
    
        # Move the mouse and perform the clicks
        try:
            autopy.mouse.move(x, y)
            autopy.mouse.click()
            autopy.mouse.move(tx, ty)
            autopy.mouse.click()
        except:
            return False
            
        if self.delay > 0:
            time.sleep(self.delay)
            
        return True
        
    
    def __eq__(self, other):
        return self.point == other.point and self.direction == other.direction and self.delay == other.delay
        
    def __str__(self):
        return "Move %s %s, delay %dms" % (self.point, self.direction.name, int(self.delay * 1000))