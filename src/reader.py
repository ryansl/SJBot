from definitions import *
from configuration import *
from benchmark import *
from board import *
import pyscreenshot as Img
import autopy


class Reader:
    def __init__(self):
        self.benchmark = Benchmark()
        
    
    # Takes a screenshot, converts it, and returns a Board object
    def get_board(self, calibration_mode = False):
        return self._convert_image_to_board(self._get_image(), calibration_mode)
        
    
    # Returns the PIL/Pillow image object from taking a screenshot at the given area
    def _get_image(self):
        image = None
        try:
            autopy.mouse.move(Configuration.idle_x, Configuration.idle_y)
            image = Img.grab(bbox = (Configuration.offset_x, Configuration.offset_y, Configuration.offset_x + Configuration.grid_size, Configuration.offset_y + Configuration.grid_size))
        except:
            image = None

        return image
    
    
    # Given a PIL/Pillow image object, determines the colors (or average RGB in calibration mode) of all gems on the grid and returns them in a Board object
    def _convert_image_to_board(self, image, calibration_mode = False):
        if image ==  None:
            return None

        pixels = image.convert("RGB")
        result = Board()
        gs = Configuration.gem_size

        # Go through each cell (every gem location) and process it
        for y in range(Configuration.grid_length):
            row = []

            for x in range(Configuration.grid_length):
                totalRed = 0
                totalGreen = 0
                totalBlue = 0
                baseX = x * gs
                baseY = y * gs
                sampleCount = gs * gs / Configuration.skip
                gemColor = None

                # Take the average of all the pixel values in the gem area
                for py in range(0, gs, Configuration.skip):
                    for px in range(0, gs, Configuration.skip):
                        rgb = pixels.getpixel((baseX + px, baseY + py))
                        totalRed += rgb[0]
                        totalGreen += rgb[1]
                        totalBlue += rgb[2]
                average = (totalRed / sampleCount, totalGreen / sampleCount, totalBlue / sampleCount)


                # Use the average to predict the color of this gem (or in calibration mode, return the average)
                if calibration_mode:
                    result[(x + 1, y + 1)] = "(" + ",".join(map(lambda s: str(s), average)) + ")"

                else:
                    for color, rgb in Configuration.color_table[Configuration.skip].iteritems():
                        test = [abs(rgb[index] - average[index]) <= Configuration.tolerance for index in range(3)]
                        if test[0] == True and test[1] == True and test[2] == True:
                            gemColor = color
                            break
    
                    result[(x + 1, y + 1)] = gemColor
                    
        return result