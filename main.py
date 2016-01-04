from definitions import *
from utility import *
from configuration import *
from benchmark import *
from board import *
from move import *
from reader import *
from strategy import *
import time
import sys

# TODO: Fix bug where the bot suddenly stops working despite matches existing

def main(args):
    reader = Reader()
    benchmark = Benchmark()
    board = None
    runOnce = False
    
    if len(args) > 1:
        for x in range(1, len(args)):
            if args[x] == "-d":    Configuration.debug = True
            elif args[x] == "-b":  Configuration.benchmark = True
            elif args[x] == "-c":  Configuration.calibrating = True
            elif args[x] == "-1":  runOnce = True
            
    if runOnce:
        time.sleep(1)
    
    while True:
        benchmark.start("main")
        
        while board == None or board.num_unknowns > Configuration.unknown_threshold:
            board = reader.get_board()
            if board.num_unknowns > board.size * board.size * 0.75:         # If we're not focused on the board, then wait
                time.sleep(1)
            
        moves = Strategy(board).decide()
        for move in moves:
            move.make()

        board = None
        
        cycle_time = benchmark.time("main")
        print_benchmark("")
        
        if runOnce:
            break
    

if __name__ == "__main__":
    main(sys.argv)