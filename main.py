from definitions import *
from utility import *
from configuration import *
from benchmark import *
from board import *
from move import *
from reader import *
from strategy import *


def main():
    reader = Reader()
    board = None
    
    time.sleep(1)       # temporary
    while True:
        while board == None or board.num_unknowns > Configuration.unknown_threshold:
            board = reader.get_board()
            print board.num_unknowns
            
        moves = Strategy(board).decide()
        for move in moves:
            print str(move)
            #move.make()
        
        break
        time.sleep(0.5)
    
if __name__ == "__main__":
    main()