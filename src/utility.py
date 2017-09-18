from definitions import *
from configuration import *


# Returns whether the given one-dimensional coordinate is within bounds
def in_bounds(coordinate):
    return coordinate != None and coordinate >= 1 and coordinate <= Configuration.grid_length
    

# Returns whether the given point is valid (in-bounds)
def valid_point(point):
    return point != None and in_bounds(point.x) and in_bounds(point.y)
    

# Prints a debug message
def print_debug(message):
    if Configuration.debug: print "[BOT] %s" % (message)


# Prints the contents of a Board
def print_board(board):
    if board == None:
        return
        
    gs = Configuration.grid_length
    for y in range(1, gs + 1):
            for x in range(1, gs + 1):
                print board[(x, y)], 
            print "\n"
            

# Returns the powerset of the current list
def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item


# Given a Point and its direction, returns the other Point that it needs to be swapped with
def get_swap_point(point, direction):
    if not valid_point(point):
        return None
        
    if direction == Direction.left:     return Point(point.x - 1, point.y)
    elif direction == Direction.right:  return Point(point.x + 1, point.y)
    elif direction == Direction.up:     return Point(point.x, point.y - 1)
    elif direction == Direction.down:   return Point(point.x, point.y + 1)
    return None
    
    
# Given a Match object, returns a list of Points in that match
def get_points_from_match(match):
    result = []
    vertical_multiplier = int(match.orientation == Orientation.vertical)
    horizontal_multiplier = int(match.orientation == Orientation.horizontal)
    
    for c in range(match.length):
        result.append(Point(match.point.x + (horizontal_multiplier * c), match.point.y + (vertical_multiplier * c)))
        
    return result