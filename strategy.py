from definitions import *
from utility import *
from configuration import *
from board import *
from move import *


class Strategy:
    def __init__(self, board):
        self.board = board
        
    
    # Returns all possible Moves that can be made on the board
    def _get_all_moves(self):
        gems = self.board.data
        gs = self.board.size
        
        if gems == None or not gems:
            return None
        
        result = []
        pairs = []
        
        # Enumerations of all pair types and direections
        Horizontal = 1
        Vertical = 2
        GapHorizontal = 3
        GapVertical = 4
        
        Right = 1
        Left = 2
        Up = 3
        Down = 4
        
        # Mapping table for old direction to new direction
        oldToNewDirection = {
            Right : Direction.right,
            Left  : Direction.left,
            Up    : Direction.up,
            Down  : Direction.down
        }
        
        # Step 1: Find all pairs (adjacent gems)
        for y in range(gs):
            for x in range(gs):
                if gems[y][x] == None:
                    continue
                
                if x < gs - 1 and gems[y][x] == gems[y][x + 1]:
                   pairs.append(((x, y), (x + 1, y), Horizontal))
            
                if y < gs - 1 and gems[y][x] == gems[y + 1][x]:
                    pairs.append(((x, y), (x, y + 1), Vertical))
                
                if x < gs - 2 and gems[y][x] == gems[y][x + 2]:
                    pairs.append(((x, y), (x + 2, y), GapHorizontal))
                
                if y < gs - 2 and gems[y][x] == gems[y + 2][x]:
                    pairs.append(((x, y), (x, y + 2), GapVertical))
    
    
        # Step 2: For each pair, if there is a gem that can fill it in, then add it to the list of moves
        for pair in pairs:
            x = pair[0][0]             # Top/Left gem
            y = pair[0][1]
            j = pair[1][0]             # Bottom/Right gem
            k = pair[1][1]
        
            # Prioritize vertical clears over horizontal clears
            if pair[2] == Vertical:
                if y > 0 and x > 0 and gems[y - 1][x - 1] == gems[y][x]:            result.append((x - 1, y - 1, Right))    # NW of top
                if y > 0 and x < gs - 1 and gems[y - 1][x + 1] == gems[y][x]:       result.append((x + 1, y - 1, Left))     # NE of top
                if k < gs - 1 and j > 0 and gems[k + 1][j - 1] == gems[k][j]:       result.append((j - 1, k + 1, Right))    # SW of bottom
                if k < gs - 1 and j < gs - 1 and gems[k + 1][j + 1] == gems[k][j]:  result.append((j + 1, k + 1, Left))     # SE of bottom
                if y >= 2 and gems[y - 2][x] == gems[y][x]:                         result.append((x, y - 2, Down))         # N of top
                if k < gs - 2 and gems[k + 2][j] == gems[k][j]:                     result.append((j, k + 2, Up))           # S of bottom
            
            if pair[2] == Horizontal:
                if x > 0 and y > 0 and gems[y - 1][x - 1] == gems[y][x]:            result.append((x - 1, y - 1, Down))     # NW of left
                if x > 0 and y < gs - 1 and gems[y + 1][x - 1] == gems[y][x]:       result.append((x - 1, y + 1, Up))       # SW of left
                if j < gs - 1 and k > 0 and gems[k - 1][j + 1] == gems[k][j]:       result.append((j + 1, k - 1, Down))     # NE of right
                if j < gs - 1 and k < gs - 1 and gems[k + 1][j + 1] == gems[k][j]:  result.append((j + 1, k + 1, Up))       # SE of right
                if x >= 2 and gems[y][x - 2] == gems[y][x]:                         result.append((x - 2, y, Right))        # W of left
                if j < gs - 2 and gems[k][j + 2] == gems[k][j]:                     result.append((j + 2, k, Left))         # E of right

            if pair[2] == GapHorizontal:
                if y > 0 and gems[y - 1][x + 1] == gems[y][x]:                      result.append((x + 1, y - 1, Down))     # N of middle gap
                if y < gs - 1 and gems[y + 1][x + 1] == gems[y][x]:                 result.append((x + 1, y + 1, Up))       # S of middle gap
        
            if pair[2] == GapVertical:
                if x > 0 and gems[y + 1][x - 1] == gems[y][x]:                      result.append((x - 1, y + 1, Right))    # W of middle gap
                if x < gs - 1 and gems[y + 1][x + 1] == gems[y][x]:                 result.append((x + 1, y + 1, Left))     # E of middle gap
        
        
        # Step 3: Remove duplicates from the list
        finalResult = []
        seen = {}
        
        for r in result:
            s = str(r)
            if not s in seen:
                finalResult.append(r)
                seen[s] = True        
                
                
        # Step 4: Convert the list of (x, y, direction) into a list of Move objects, and return it
        return [Move(Point(r[0] + 1, r[1] + 1), oldToNewDirection[r[2]]) for r in finalResult]
        
    
    # Using the board data, compute the best non-conflicting set of moves that maximize the score and return them as a list of Moves
    def decide(self):
        
        """
        Algorithm description:
        ----------------------------------
        1. Determine all possible moves (which may conflict)
        2. Compute the total points (primary metric) for each individual move
        3. Order the moves from highest to lowest number of points
        4. Find the best set of non-conflicting moves that maximizes the number of points earned
        """
        return self._get_all_moves()
        
        
        
        