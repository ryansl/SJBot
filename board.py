from definitions import *
from utility import *
from configuration import *


class Board:
    def __init__(self):
        self.data = []
        self.size = Configuration.grid_length
        self.num_unknowns = 0
        self.clear()
        
    def clear(self):
        self.data = [[None for x in range(self.size)] for y in range(self.size)] if self.size > 0 else None
        
    def swap(self, pa, pb):
        if not valid_point(pa) or not valid_point(pb):
            return False
            
        temp = self.data[pa.y - 1][pa.x - 1]
        self.data[pa.y - 1][pa.x - 1] = self.data[pb.y - 1][pb.x - 1]
        self.data[pb.y - 1][pb.x - 1] = temp
        return True
        
    def get_matches(self):
        # TODO: Implement this
        pass
        
    def __getitem__(self, point):
        (x, y) = point
        return self.data[y - 1][x - 1] if in_bounds(x) and in_bounds(y) else None
        
    def __setitem__(self, point, value):
        (x, y) = point
        if in_bounds(x) and in_bounds(y):
            if self.data[y - 1][x - 1] == None:
                self.num_unknowns -= 1
                
            if value == None:
                self.num_unknowns += 1
                
            self.data[y - 1][x - 1] = value
            
    def __delitem__(self, point):
        (x, y) = point
        if not in_bounds(x) or not in_bounds(y):
            return
            
        for v in range(y - 1, 0, -1):
            self.data[v][x - 1] = self.data[v - 1][x - 1]
            
        self.data[0][x] = None
        self.num_unknowns += 1
            