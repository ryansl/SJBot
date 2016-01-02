from definitions import *
from utility import *
from configuration import *
import copy
import sys


class Board:
    def __init__(self):
        self.data = []
        self.size = Configuration.grid_length
        self.num_unknowns = 0
        self.backup_data = None
        self.backup_num_unknowns = None
        self.clear()
        
    
    # Reset all elements on the board back to unknowns
    def clear(self):
        self.data = [[None for x in range(self.size)] for y in range(self.size)] if self.size > 0 else None
        
        
    # Make a backup of the internal data
    def _backup(self):
        self.backup_data = copy.deepcopy(self.data)
        self.backup_num_unknowns = self.num_unknowns
        
        
    # Restore data from the backup
    def _restore(self):
        if self.backup_data == None or self.backup_num_unknowns == None:
            return
        
        self.data = copy.deepcopy(self.backup_data)
        self.num_unknowns = self.backup_num_unknowns
        self.backup_data = None
        self.backup_num_unknowns = None
    
        
    # Swap two gems on the board
    def swap(self, pa, pb):
        if not valid_point(pa) or not valid_point(pb):
            return False
            
        temp = self.data[pa.y - 1][pa.x - 1]
        self.data[pa.y - 1][pa.x - 1] = self.data[pb.y - 1][pb.x - 1]
        self.data[pb.y - 1][pb.x - 1] = temp
        return True
        
        
    # Return a list of all Matches on the board
    def get_matches(self):
        gs = self.size
        matches = []
        current = None
        length = 0
        
        # Find horizontal matches
        for y in range(gs):
            for x in range(gs):
                if self.data[y][x] == current:
                    length += 1
                    
                if self.data[y][x] != current or x == gs - 1:
                    if length >= 3 and current != None:
                        matches.append(Match(Point(x - length + 1 if x < gs - 1 else gs - length + 1, y + 1), current, Orientation.horizontal, length, Configuration.points_table[length]))
                        
                    current = self.data[y][x]
                    length = 1
                    
            length = 0
            current = None
            
            
        # Find vertical matches
        for x in range(gs):
            for y in range(gs):
                if self.data[y][x] == current:
                    length += 1
                    
                if self.data[y][x] != current or y == gs - 1:
                    if length >= 3 and current != None:
                        matches.append(Match(Point(x + 1, y - length + 1 if y < gs - 1 else gs - length + 1), current, Orientation.vertical, length, Configuration.points_table[length]))
                        
                    current = self.data[y][x]
                    length = 1
                    
            length = 0
            current = None
                            
        return matches
        
        
    # Remove all matches from the board and shift down accordingly
    def remove_matches(self, matches = None):
        if matches == None:
            matches = self.get_matches()
            
        for match in matches:
            points = get_points_from_match(match)
            for point in points:
                del self[point.to_tuple()]
            
        
    
    # Return the list of all Matches created if we swapped these two gems on the board, including chains (does not change the board)
    def stimulate_swap(self, pa, pb):
        if not valid_point(pa) or not valid_point(pb):
            return None
        
        result = []
        chain_level = 1
            
        self._backup()
        self.swap(pa, pb)
        
        while True:
            matches = self.get_matches()
            for m in matches:
                m.update_chain_level(chain_level)
                
            self.remove_matches(matches)
            result += matches
            chain_level += 1
            
            if len(matches) == 0:
                break
        
        self._restore()
        return result
        
        
    # Return value at position on the board
    def __getitem__(self, point):
        (x, y) = point
        return self.data[y - 1][x - 1] if in_bounds(x) and in_bounds(y) else None
        
        
    # Set value at position on the board
    def __setitem__(self, point, value):
        (x, y) = point
        if in_bounds(x) and in_bounds(y):
            if self.data[y - 1][x - 1] == None:
                self.num_unknowns -= 1
                
            if value == None:
                self.num_unknowns += 1
                
            self.data[y - 1][x - 1] = value
        return value
            
            
    # Remove the gem at the given position and shift gems above it down
    def __delitem__(self, point):
        (x, y) = point
        if not in_bounds(x) or not in_bounds(y):
            return
            
        for v in range(y - 1, 0, -1):
            self.data[v][x - 1] = self.data[v - 1][x - 1]
            
        self.data[0][x - 1] = None
        self.num_unknowns += 1
        return None
            