from definitions import *


class Configuration:
    offset_x = 930              # X offset of grid
    offset_y = 85               # Y offset of grid
    grid_size = 480             # Size of grid (square)
    gem_size = 60               # Size of gem (square)
    grid_length = 8             # Number of gems from top-bottom or left-right
    chain_multiplier = 2        # Multiplier for chains of matches (eg: matching a gem, other gems fall, another match automatically happens)
    
    idle_x = 500                # X offset for idle position
    idle_y = 200                # Y offset for idle position

    tolerance = 3               # RGB tolerance range for gem color detection
    skip = 5                    # Percentage (100 / skip %) of pixels averaged to determine gem color (higher = slower, but more accurate)
    unknown_threshold = 32      # Max number of unknown gems allowed before converting board
    
    debug = False               # Runtime flag -- show debug output
    benchmark = False           # Runtime flag -- show performance data
    calibrating = False         # Runtime flag -- show average RGB values when converting image to map
    
    # Color mapping table -- maps skip -> ([color -> average rgb value])
    color_table = {
        5 : {
            Color.white  : (15, 14, 14),
            Color.red    : (21, 7, 4),
            Color.blue   : (14, 28, 35),
            Color.purple : (15, 8, 17),
            Color.green  : (13, 25, 7),
            Color.yellow : (22, 22, 10)
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