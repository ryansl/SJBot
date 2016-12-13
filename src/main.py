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

    if len(args) > 1:
        for x in range(1, len(args)):
            if args[x] == "-d":    Configuration.debug = True
            elif args[x] == "-b":  Configuration.benchmark = True
            elif args[x] == "-c":  Configuration.calibrating = True

    if Configuration.look_ahead_count < 1:
        print "Error: look_ahead_count in configuration must be at least 1"
        return False


    # Calibration mode?
    if Configuration.calibrating:
        raw_input("Calibration Mode - Open SC2 window or image in fullscreen, then press Enter: \n")
        print_debug("Board color averages")
        print_board(reader.get_board(True))
        print_debug("Board color estimates")
        print_board(reader.get_board(False))
        return True


    # Separate thread for handling start/stop controls
    toggle_thread = threading.Thread(target = enable_toggle)
    toggle_thread.daemon = True
    toggle_thread.start()


    # Main loop
    while True:
        if not Configuration.enabled:
            time.sleep(0.1)
            continue

        # Keep reading the board until we get an accurate representation of it
        benchmark.start("main")
        board = reader.get_board()
        while Configuration.enabled and (board == None or board.num_unknowns > Configuration.unknown_threshold):
            board = reader.get_board()
            time.sleep(0.25)


        # Decide which moves to make and execute them
        benchmark.start("decision")
        move_set = Strategy(board).decide()
        decide_time = benchmark.time("decision")
        move_set.make()
        total_time = benchmark.time("main")
        board = None


        # Print benchmark information
        if Configuration.benchmark:
            print_debug("Total time: %f" % (total_time))
            print_debug("Decision time: %f" % (decide_time))
            print_debug("-----------------------")

    return True
    
    
# Call main
if __name__ == "__main__":
    main(sys.argv)