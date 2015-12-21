import sys
import os
import time
import datetime
import math
import pyscreenshot as Img
import autopy


# OPTIMIZATION IDEAS:
# 3. Eliminate operations on conflicting pairs -> make it so that all decisions will succeed
# 4. Smarter pattern matching, prioritizing wider rows

# Configuration variables
OFFSET_X = 930
OFFSET_Y = 85
GRID_SIZE = 480
GRID_COUNT = 8
GEM_SIZE = GRID_SIZE / GRID_COUNT
SPELL_X = 500
SPELL_Y = 200

TOLERANCE = 5
SKIP = 5
UNKNOWN_THRESHOLD = GRID_COUNT
RESET_SECONDS = 3
# ----------------------

# Enabled flag
Enabled = True

# Colors
Unknown = 0
White = 1
Red = 2
Blue = 3
Purple = 4
Green = 5
Yellow = 6

# Directions
Left = 1
Right = 2
Up = 3
Down = 4

# Pair Orientations
Horizontal = 1
Vertical = 2

# Gem color index to RGB average value
GemToColor = {
     1 : (15, 14, 14),
     2 : (21, 7, 4),
     3 : (14, 28, 35),
     4 : (15, 8, 17),
     5 : (13, 25, 7),
     6 : (22, 22, 10)
}

# Gem color index to text
ColorToText = {
    0 : "?????",
    1 : "White",
    2 : "Red",
    3 : "Blue",
    4 : "Purple",
    5 : "Green",
    6 : "Yellow"
}

# Direction to text
DirectionToText = {
    1: "Left",
    2: "Right",
    3: "Up",
    4: "Down"
}


# Given an image, outputs an NxN list of the gem colors and the number of unknowns
def imageToMap(image):
    if image is None or not image:
        return (None, 0)
        
    # Convert the image to a 2D list of RGB tuple values
    try:
        pixels = image.convert("RGB")
    except:
        return (None, 0)
        
        
    # Result to be returned (two-dimensional list)
    result = []
    unknownCount = 0
        
    
    # Go through each cell (every gem location) and process it
    for y in range(GRID_COUNT):
        row = []
        
        for x in range(GRID_COUNT):
            totalRed = 0
            totalGreen = 0
            totalBlue = 0
            baseX = x * GEM_SIZE
            baseY = y * GEM_SIZE
            sampleCount = GEM_SIZE * GEM_SIZE / SKIP
            gemColor = Unknown
            
            
            # Take the average of all the pixel values in the gem area
            for py in range(0, GEM_SIZE, SKIP):
                for px in range(0, GEM_SIZE, SKIP):
                    rgb = pixels.getpixel((baseX + px, baseY + py))
                    totalRed += rgb[0]
                    totalGreen += rgb[1]
                    totalBlue += rgb[2]
            average = (totalRed / sampleCount, totalGreen / sampleCount, totalBlue / sampleCount)
            
            
            # Use the average to predict the color of this gem
            for color, rgb in GemToColor.iteritems():
                test = [abs(rgb[index] - average[index]) <= TOLERANCE for index in range(3)]
                if test[0] == True and test[1] == True and test[2] == True:
                    gemColor = color
                    break
                    
            
            # If the color is still unknown, then record it
            if gemColor == Unknown:
                unknownCount += 1
                
            row.append(gemColor)
        result.append(row)
        
        
    # We are done!
    return (result, unknownCount)
    
    
# Convert a 2D map of colors to their text equivalents
def mapColorToText(colors):
    if colors == None or not colors:
        return None
        
    return [[ColorToText[color] for color in row] for row in colors]
    
    
# Given a map of gem colors, decides the set of gems to move (multiple possible) and return them as [(x, y, DIRECTION), ...]
def makeDecisions(gems):
    if gems == None or not gems:
        return None
        
    result = []
    pairs = []
    
    # Step 1: Find all pairs (adjacent gems)
    for y in range(GRID_COUNT):
        for x in range(GRID_COUNT):
            if x < GRID_COUNT - 1 and gems[y][x] == gems[y][x + 1] and gems[y][x] != Unknown:
                pairs.append(((x, y), (x + 1, y), Horizontal))
            
            if y < GRID_COUNT - 1 and gems[y][x] == gems[y + 1][x] and gems[y][x] != Unknown:
                pairs.append(((x, y), (x, y + 1), Vertical))
    
    
    # Step 2: For each pair, if there is a gem that can fill it in, then add it to the decision list
    for pair in pairs:
        x = pair[0][0]             # Top/Left gem
        y = pair[0][1]
        j = pair[1][0]             # Bottom/Right gem
        k = pair[1][1]
        
        if pair[2] == Horizontal:
            if x > 0 and y > 0 and gems[y - 1][x - 1] == gems[y][x]:                            result.append((x - 1, y - 1, Down))     # NW of left
            if x > 0 and y < GRID_COUNT - 1 and gems[y + 1][x - 1] == gems[y][x]:               result.append((x - 1, y + 1, Up))       # SW of left
            if x >= 2 and gems[y][x - 2] == gems[y][x]:                                         result.append((x - 2, y, Right))        # W of left
            if j < GRID_COUNT - 1 and k > 0 and gems[k - 1][j + 1] == gems[k][j]:               result.append((j + 1, k - 1, Down))     # NE of right
            if j < GRID_COUNT - 1 and k < GRID_COUNT - 1 and gems[k + 1][j + 1] == gems[k][j]:  result.append((j + 1, k + 1, Up))       # SE of right
            if j < GRID_COUNT - 2 and gems[k][j + 2] == gems[k][j]:                             result.append((j + 2, k, Left))         # E of right
            
        elif pair[2] == Vertical:
            if y > 0 and x > 0 and gems[y - 1][x - 1] == gems[y][x]:                            result.append((x - 1, y - 1, Right))    # NW of top
            if y > 0 and x < GRID_COUNT - 1 and gems[y - 1][x + 1] == gems[y][x]:               result.append((x + 1, y - 1, Left))     # NE of top
            if y >= 2 and gems[y - 2][x] == gems[y][x]:                                         result.append((x, y - 2, Down))         # N of top
            if k < GRID_COUNT - 1 and j > 0 and gems[k + 1][j - 1] == gems[k][j]:               result.append((j - 1, k + 1, Right))    # SW of bottom
            if k < GRID_COUNT - 1 and j < GRID_COUNT - 1 and gems[k + 1][j + 1] == gems[k][j]:  result.append((j + 1, k + 1, Left))     # SE of bottom
            if k < GRID_COUNT - 2 and gems[k - 2][j] == gems[k][j]:                             result.append((j, k - 2, Up))           # S of bottom
    
    return result
    
    
# Control the mouse and use it to swap the gem for a decision
def processDecision(decision):
    if decision == None or not decision:
        return
        
    # Compute the coordinates of the starting and ending clicks
    x = int(math.floor(OFFSET_X + (decision[0] * GEM_SIZE) + (GEM_SIZE / 2)))
    y = int(math.floor(OFFSET_Y + (decision[1] * GEM_SIZE) + (GEM_SIZE / 2)))
    dx = 0
    dy = 0
    tx = 0
    ty = 0
    
    if decision[2] == Up:       dy = -1
    elif decision[2] == Down:   dy = 1
    elif decision[2] == Left:   dx = -1
    elif decision[2] == Right:  dx = 1
    
    tx = x + (dx * GEM_SIZE)
    ty = y + (dy * GEM_SIZE)
    
    
    # If the starting or ending mouse position is not in the grid, then don't try to move
    # NOTE: Exceptions are really expensive! They cost about 100ms of time
    w = OFFSET_X + GRID_SIZE
    h = OFFSET_Y + GRID_SIZE
    
    if x < OFFSET_X or y < OFFSET_Y or tx < OFFSET_X or ty < OFFSET_Y or x > w or y > h or tx > w or ty > h:
        return
    
    
    # Move the mouse and perform the clicks
    try:
        autopy.mouse.move(x, y)
        autopy.mouse.click()
        autopy.mouse.move(tx, ty)
        autopy.mouse.click()
    except:
        pass
        
    
# Enable the bot (on UP keypress)            
def enableBot():
    global Enabled
    Enabled = True
    

# Disable the bot (on DOWN keypress)
def disableBot():
    global Enabled
    Enabled = False
    
    
# Main function, entrypoint of the application
if __name__ == "__main__":
    print "Welcome to the StarJeweled AutoBot"
    print "Press UP to start, or DOWN to stop"
    
    # Main application loop
    while True:
        if not Enabled:
            time.sleep(0.2)
            continue
            
        lastDecision = None
        before = datetime.datetime.now()
        grid = None
        
        
        # Get the screen data
        try:
            grid = Img.grab(bbox = (OFFSET_X, OFFSET_Y, OFFSET_X + GRID_SIZE, OFFSET_Y + GRID_SIZE))
        except:
            grid = None
            
        if grid == None:
            print "Error getting screen data"
            continue
            
        
        # Convert it to a gem map
        try:
            (gems, unknownCount) = imageToMap(grid)
        except:
            gems = None
            
        if gems == None:
            print "Error converting grid to gem map"
            continue
            
        if unknownCount >= UNKNOWN_THRESHOLD:
            print "Found %d unknowns, skipping because there are too many" % (unknownCount)
            continue
        
        
        # Build a set of decisions
        decisions = makeDecisions(gems)
        if decisions == None:
            print "Error making decisions"
            continue
    
    
        # Process the decisions
        if len(decisions) > 0:
            for d in decisions:
                print "Move gem (%d, %d) %s" % (d[0] + 1, d[1] + 1, DirectionToText[d[2]])
                processDecision(d)
                
            lastDecision = datetime.datetime.now()
            autopy.mouse.move(SPELL_X, SPELL_Y)
            
        # If there are no decisions and we haven't made a decision in 3 seconds, then reset the board
        else:
            if lastDecision != None and (datetime.datetime.now() - lastDecision).seconds >= RESET_SECONDS:
                autopy.key.tap("z")
            print "No decisions could be made"
    
    
        # Benchmarking for testing purposes
        after = datetime.datetime.now()
        seconds = (after - before).microseconds / 1e6
        print "Finished computation in %f seconds" % (seconds)