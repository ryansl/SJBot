from definitions import *
from utility import *
from configuration import *
from board import *
from move import *
import copy
import itertools


class Strategy:
    def __init__(self, board, look_ahead_counter = Configuration.look_ahead_count):
        self.board = board
        self.look_ahead_counter = look_ahead_counter
        
    
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
        all_moves = self._get_all_moves()       # All moves
        move_count = len(all_moves)             # Number of all moves
        move_dictionary = {}                    # Maps MoveID -> MoveObject
        move_info = {}                          # Maps MoveID -> (Points, ChainLength, NumMovesCreated)]
        move_score = {}                         # Maps MoveID -> MoveScore (where MoveScore is a score computed from the three metrics)
        move_counter = 0                        # Incremented by one for every move, provides the move ID


        # Assign each move a unique ID to identify it to be used as a key for the dictionaries
        for move in all_moves:
            move_dictionary[move_counter] = move
            move_counter += 1


        # Compute the three metrics for each move (points, chain length, and number of moves created)
        for id in range(move_count):
            total_points = 0
            max_chain_length = 1

            move = move_dictionary[id]
            swap_point = get_swap_point(move.point, move.direction)
            match_set = self.board.stimulate_swap(move.point, swap_point)

            for match in match_set:
                total_points += match.points
                max_chain_length = match.chain_level if match.chain_level > max_chain_length else max_chain_length

            next_board = copy.deepcopy(self.board)
            next_board.swap(move.point, swap_point)
            next_board.remove_matches()

            strategy = Strategy(next_board)
            num_moves_created = len(strategy._get_all_moves())
            move_info[id] = (total_points, max_chain_length, num_moves_created)


        # Calculate a score for each move based on a calculation of the three metrics
        for move_id, info in move_info.iteritems():
            move_score[move_id] = info[0] + (info[2] * 5)       # points_gained + (num_moves_created * 5)


        # Order the moves from best move to worst move (based on score) and return them as a MoveSet with delays added
        moves = []
        total_points = 0
        highest_chain = 0

        for move_id in sorted(move_score, key = move_score.get, reverse = True):
            moves.append(move_dictionary[move_id])
            total_points += move_info[move_id][0]
            highest_chain = move_info[move_id][1] if move_info[move_id][1] > highest_chain else highest_chain

        return MoveSet(moves, total_points, (highest_chain - 1) * Configuration.chain_delay)