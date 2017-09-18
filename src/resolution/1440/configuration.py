from definitions import *

"""
Grid positions for 1440p:
    (1740, 134) to (2508, 902)
"""

class Configuration:
    screen_width = 2560         # Width of computer screen
    screen_height = 1440        # Height of computer screen

    offset_x = 1740             # X offset of grid
    offset_y = 134              # Y offset of grid
    grid_size = 768             # Size of grid (square)
    gem_size = 96               # Size of gem (square)
    grid_length = 8             # Number of gems from top-bottom or left-right

    idle_x = 1050                # X offset for idle position
    idle_y = 800                 # Y offset for idle position

    tolerance = 3               # RGB tolerance range for gem color detection
    skip = 5                    # Percentage (100 / skip %) of pixels averaged to determine gem color (higher = slower, but more accurate)
    unknown_threshold = 48      # Max number of unknown gems allowed before converting board
    look_ahead_count = 3        # Look ahead X number of moves to find the best move
    chain_delay = 0.25          # Number of seconds to delay for each chain level above one
    powerset_limit = 5          # Maximum number of moves we can calculate powerset for without hindering performance

    enabled = False             # Runtime flag -- run the bot algorithm?
    debug = False               # Runtime flag -- show debug output
    benchmark = False           # Runtime flag -- show performance data
    calibrating = False         # Runtime flag -- show average RGB values when converting image to map


    # Color mapping table -- maps skip -> ([color -> average rgb value])
    color_table = {
        5 : {
            Color.white  : (16, 16, 15),
            Color.red    : (24, 10, 6),
            Color.blue   : (13, 28, 34),
            Color.purple : (15, 8, 15),
            Color.green  : (15, 26, 8),
            Color.yellow : (23, 22, 10)
        }
    }
    
    
    # Points mapping table -- maps match_length -> points
    points_table = {
        3 : 30,
        4 : 60,
        5 : 120,
        6 : 240,
        7: 480,
        8: 960
    }