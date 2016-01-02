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
        board.data = [
            [Color.red, None, None, None, None],
            [Color.red, None, None, None, None],
            [Color.green, None, None, None, None],
            [Color.red, None, None, None, None],
            [Color.red, Color.green, Color.green, Color.yellow, Color.yellow]
            
        ]
        board.size = 5
        print board.stimulate_swap(Point(1, 2), Point(1, 3))
        break
        
        moves = Strategy(board).decide()
        
        for move in moves:
            print move
            #move.make()
            
        time.sleep(0.5)
    
if __name__ == "__main__":
    main()