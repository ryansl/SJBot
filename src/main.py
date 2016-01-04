from definitions import *
from utility import *
from configuration import *
from benchmark import *
from board import *
from move import *
from reader import *
from strategy import *
import autopy
import threading
import time
import sys


# Enables or disables the bot depending on where the mouse is
def enable_toggle():
    while True:
        (x, y) = autopy.mouse.get_pos()

        # Move mouse to top right corner to start the bot
        if x > Configuration.screen_width - 5 and y == 0:
            print_debug("Bot Enabled")
            Configuration.enabled = True

        # Move mouse to top left corner to stop the bot
        elif x < 5 and y == 0:
            print_debug("Bot Disabled")
            Configuration.enabled = False

        time.sleep(0.1)


# Main function, entrypoint of the application
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
    else:
        toggle_thread = threading.Thread(target = enable_toggle)
        toggle_thread.daemon = True
        toggle_thread.start()


    while True:
        if not Configuration.enabled:
            time.sleep(0.1)
            continue

        print_debug("Starting iteration %d" % (counter))
        benchmark.start("main")

        while not runOnce and (board == None or board.num_unknowns > Configuration.unknown_threshold):
            if not Configuration.enabled:
                time.sleep(0.1)
                continue

            board = reader.get_board()
            if board.num_unknowns >= board.size * board.size * 0.75:
                time.sleep(1)
                continue

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