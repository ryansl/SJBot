from definitions import *
from utility import *
from configuration import *
from benchmark import *
from board import *
from move import *
from reader import *
from strategy import *
import time


# TODO: Fix bug where the bot suddenly stops working despite matches existing

def main():
    reader = Reader()
    board = None
    
    while True:
        while board == None or board.num_unknowns > Configuration.unknown_threshold:
            board = reader.get_board()
            if board.num_unknowns > board.size * board.size * 0.75:         # If we're not focused on the board, then wait
                time.sleep(1)
            
        moves = Strategy(board).decide()
        for move in moves:
            move.make()

        board = None
    

if __name__ == "__main__":
    main()