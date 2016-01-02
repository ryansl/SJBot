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
    
    time.sleep(1)
    while True:
        board = reader.get_board()
        moves = Strategy(board).decide()
        
        for move in moves:
            print str(move)
            #move.make()
        
        break
        time.sleep(0.5)
    
if __name__ == "__main__":
    main()