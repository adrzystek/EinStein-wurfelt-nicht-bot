import numpy as np
import random


class Board():
    
    def __init__(self, given_board=None, board_size=5):
        self.given_board = given_board
        self.board_size = board_size
        self.starting_positions_red = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]
        self.starting_positions_blue = [(4, 4), (4, 3), (4, 2), (3, 4), (3, 3), (2, 4)]
        
    def initialize(self):
        if self.given_board is None:
            board = np.zeros((self.board_size, self.board_size), int)
            random.shuffle(self.starting_positions_red)
            random.shuffle(self.starting_positions_blue)
            for i in range(len(self.starting_positions_blue)):
                board[self.starting_positions_red[i]] = -(i+1)
                board[self.starting_positions_blue[i]] = i+1
        else:
            board = self.given_board.copy()
        pieces_position = {}
        pieces = board[board != 0]
        for p in pieces:
            row, col = np.where(board == p)
            row, col = row[0], col[0]
            pieces_position[p] = (row, col)
        return board, pieces_position
        

class Player():
    
    def __init__(self, color, board_size=5):
        self.color = color
        self.board_size = board_size
        self.won = False
        
    def get_possible_pieces(self, dice, pieces_position):
        pieces = [k for k in pieces_position.keys() if k * dice > 0]
        pieces_to_play = []
        if dice in pieces:
            pieces_to_play.append(dice)
        else:
            _pieces = pieces + [dice]
            _pieces.sort()
            _index = _pieces.index(dice)
            if _index == 0:
                pieces_to_play.append(_pieces[_index+1])
            elif _index == len(_pieces)-1:
                pieces_to_play.append(_pieces[_index-1])
            else:
                pieces_to_play.append(_pieces[_index-1])
                pieces_to_play.append(_pieces[_index+1])
        return pieces_to_play
    
    def get_feasible_moves(self, piece, pieces_position):
        row, col = pieces_position[piece]
        if self.color == 'blue':
            feasible_moves = []
            if row != 0:
                feasible_moves.append((row-1, col))
            if col != 0:
                feasible_moves.append((row, col-1))
            if row != 0 and col != 0:
                feasible_moves.append((row-1, col-1))
        elif self.color == 'red':
            feasible_moves = []
            if row != self.board_size-1:
                feasible_moves.append((row+1, col))
            if col != self.board_size-1:
                feasible_moves.append((row, col+1))
            if row != self.board_size-1 and col != self.board_size-1:
                feasible_moves.append((row+1, col+1))
        return feasible_moves
    
    def roll_dice(self, given_dice=None):
        if given_dice is None:
            dice = random.choice(range(1, self.board_size+2))
        else:
            dice = given_dice
        if self.color == 'red':
            dice = -dice
        return dice
            
    def choose_piece_and_position(self, pieces_position, board, given_dice=None, thrs=0.5):
        dice = self.roll_dice(given_dice)
        possible_pieces = self.get_possible_pieces(dice, pieces_position)
        if random.random() < thrs:
            piece_move_assessment = {}
            for piece in possible_pieces:
                feasible_moves = self.get_feasible_moves(piece, pieces_position)
                for move in feasible_moves:
                    _pieces_position = self.make_move(piece, move, pieces_position, board, dummy=True)
                    piece_move_assessment[(piece, move)] = self.assess_position(_pieces_position)
            if self.color == 'blue':
                (best_piece, best_position), position_assessment = sorted(piece_move_assessment.items(), key = lambda x: x[1], reverse=False)[0]
            else:
                (best_piece, best_position), position_assessment = sorted(piece_move_assessment.items(), key = lambda x: x[1], reverse=True)[0]
        else:
            best_piece = random.choice(possible_pieces)
            feasible_moves = self.get_feasible_moves(best_piece, pieces_position)
            best_position = random.choice(feasible_moves)
        return best_piece, best_position
    
    def make_move(self, piece, new_position, pieces_position, board, dummy=False):
        if dummy:
            _pieces_position = pieces_position.copy()
        current_position = pieces_position[piece]
        previous_piece_here = board[new_position]
        if previous_piece_here != 0:
            if dummy:
                del _pieces_position[previous_piece_here]
            else:
                del pieces_position[previous_piece_here]
        if dummy:
            _pieces_position[piece] = new_position
            return _pieces_position
        else:
            board[current_position] = 0
            board[new_position] = piece
            pieces_position[piece] = new_position
        
    def check_if_win(self, position, pieces_position):
        if self.color == 'blue' and (position == (0, 0) or not [k for k in pieces_position.keys() if k < 0]) or \
           self.color == 'red' and (position == (self.board_size-1, self.board_size-1) or not [k for k in pieces_position.keys() if k > 0]):
            self.won = True
        
    def play(self, board, pieces_position, given_piece_and_position=None):
        if given_piece_and_position is None:
            piece, new_position = self.choose_piece_and_position(pieces_position, board)
        else:
            piece = given_piece_and_position[0]
            new_position = given_piece_and_position[1]
        self.make_move(piece, new_position, pieces_position, board)
        self.check_if_win(new_position, pieces_position)
        
    def simulate_n_of_rounds_needed(self, fields_to_win, frequency, n_iter=1000000):
        """
        probability = frequency / 6
        rounds_needed = []
        for i in range(n_iter):
            n = 0
            _moves_to_win = fields_to_win
            while _moves_to_win > 0:
                if random.random() < probability:
                    _moves_to_win -= 1
                n += 1
            rounds_needed.append(n)
        return np.mean(rounds_needed)
        """
        ftw_freq_results = {(0, 1): 0.0,
                            (0, 2): 0.0,
                            (0, 3): 0.0,
                            (0, 4): 0.0,
                            (0, 5): 0.0,
                            (0, 6): 0.0,
                            (1, 1): 6.0009309999999996,
                            (1, 2): 2.9987849999999998,
                            (1, 3): 1.998707,
                            (1, 4): 1.499573,
                            (1, 5): 1.1993100000000001,
                            (1, 6): 1.0,
                            (2, 1): 11.992832,
                            (2, 2): 5.9974470000000002,
                            (2, 3): 3.9990749999999999,
                            (2, 4): 3.0004469999999999,
                            (2, 5): 2.4013450000000001,
                            (2, 6): 2.0,
                            (3, 1): 17.993707000000001,
                            (3, 2): 8.9979700000000005,
                            (3, 3): 5.9997550000000004,
                            (3, 4): 4.4966400000000002,
                            (3, 5): 3.5995119999999998,
                            (3, 6): 3.0,
                            (4, 1): 23.99136,
                            (4, 2): 12.005134999999999,
                            (4, 3): 8.004804,
                            (4, 4): 5.9971519999999998,
                            (4, 5): 4.8017149999999997,
                            (4, 6): 4.0}
        return ftw_freq_results[(fields_to_win, frequency)]
        
    def assess_position(self, pieces_position):
        avg_rounds_to_win = {}
        for _color in ['blue', 'red']:
            if _color == 'blue':
                pieces = sorted([k for k in pieces_position.keys() if k > 0])
            elif _color == 'red':
                pieces = sorted([-1 * k for k in pieces_position.keys() if k < 0])
            rounds_to_win_per_piece = []
            for i, piece in enumerate(pieces):
                if _color == 'blue':
                    fields_to_win = max(pieces_position[piece])
                elif _color == 'red':
                    fields_to_win = -min(pieces_position[-piece]) + 4
                if fields_to_win == 0:
                    rounds_to_win_per_piece.append(0)
                else:
                    if len(pieces) == 1:
                        frequency = 6
                    elif i == 0:
                        frequency = (pieces[i+1] - 1)
                    elif i == len(pieces)-1:
                        frequency = (6 - pieces[i-1])
                    else:
                        frequency = (pieces[i+1] - pieces[i-1] - 1)
                    rounds_to_win_per_piece.append(self.simulate_n_of_rounds_needed(fields_to_win, frequency))
            avg_rounds_to_win[_color] = np.mean(rounds_to_win_per_piece)
        return avg_rounds_to_win['blue'] - avg_rounds_to_win['red']
