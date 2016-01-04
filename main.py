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
    counter = 1

    if len(args) > 1:
        for x in range(1, len(args)):
            if args[x] == "-d":    Configuration.debug = True
            elif args[x] == "-b":  Configuration.benchmark = True
            elif args[x] == "-c":  Configuration.calibrating = True
            elif args[x] == "-1":  runOnce = True
            
    if runOnce:
        time.sleep(1)
    
    while True:
        print_debug("Starting iteration %d" % (counter))
        benchmark.start("main")
        
        while not runOnce and (board == None or board.num_unknowns > Configuration.unknown_threshold):
            board = reader.get_board()
            if board.num_unknowns > board.size * board.size * 0.75:         # If we're not focused on the board, then wait
                time.sleep(1)

        if board != None:
            benchmark.start("decision")
            moves = Strategy(board).decide()
            decide_time = benchmark.time("decision")
            print_benchmark("Deciding took %f seconds" % (decide_time))

            benchmark.start("move")
            for move in moves:
                print_debug("Making move: %s" % (str(move)))
                move.make()

            move_time = benchmark.time("move")
            print_benchmark("Moving took %f seconds" % (move_time))

            cycle_time = benchmark.time("main")
            print_benchmark("Total %f seconds" % (cycle_time))
            print_debug("Ending iteration %d \n" % (counter))

        else:
            print_debug("Invalid board, skipping iteration %d" % (counter))

        board = None
        counter += 1

        if runOnce:
            break
    

if __name__ == "__main__":
    main(sys.argv)