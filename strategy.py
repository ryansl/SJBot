from definitions import *
from utility import *
from configuration import *
from board import *
from move import *


class Strategy:
    def __init__(self, board):
        self.board = board
        
        
    # Using the board data, compute the best set of moves that don't conflict with each other and return them as a list of Moves
    def decide(self):
        return []