import copy
import math
import time

EMPTY_CELL = -1
LEFT_BORDER = 0
RIGHT_BORDER = 7

TIME_LIMIT = 0.99    # time spent searching for a move
DEPTH = 3         # depth of search for possible moves


class MyPlayer:
    """Player plays Alpha-beta pruning method"""

    def __init__ (self, my_color, opponent_color):
        self.name = 'klimoval'
        self.my_color = my_color
        self.op_color = opponent_color

    def move (self, board):
        # the timer starts
        self.start_time = time.time ()

        # returning the move found using Alpha-beta pruning method
        my_move = self.alpha_beta_pruning (board, DEPTH, -math.inf, math.inf, True)[0]
        return my_move

    def alpha_beta_pruning (self, board, depth, alpha, beta, my_player):
        # alpha represents the minimum score that my player can get
        # beta represents the maximum score that opponent's player can get

        if depth == 0:  # if the search depth is 0, the final score is returned
            return None, self.my_terminal_score (board)
        # moves for my player does not exist:
        if my_player:
            if not self.find_all_correct_moves (board, self.my_color, self.op_color):
                return None, -math.inf
        # moves for opponent's player does not exist:
        elif not self.find_all_correct_moves (board, self.op_color, self.my_color):
            return None, math.inf

        if my_player:
            score = -math.inf  # this value is less than any possible score
            correct_moves = self.find_all_correct_moves (board, self.my_color, self.op_color)
            my_move = correct_moves[0]  # assign the first possible move

            for move in correct_moves:
                board_copy = copy.deepcopy (board)
                self.make_move (board_copy, move, self.my_color, self.op_color)
                new_score = self.alpha_beta_pruning (board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > score:  # searching for the maximum possible score
                    score = new_score
                    my_move = move
                if score > alpha:  # searching for the maximum
                    alpha = score   # among the minimum scores
                if alpha >= beta:
                    break
                finish_time = time.time ()  # the timer stops
                elapsed_time = finish_time - self.start_time  # time spent in this move
                if elapsed_time > TIME_LIMIT:
                    break
            return my_move, score
        else:  # opponent's player
            score = math.inf  # this value is more than any possible score
            correct_moves = self.find_all_correct_moves (board, self.op_color, self.my_color)
            my_move = correct_moves[0]  # assign the first possible move

            for move in correct_moves:
                board_copy = copy.deepcopy (board)
                self.make_move (board_copy, move, self.op_color, self.my_color)
                new_score = self.alpha_beta_pruning (board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < score:  # searching for the minimum possible score
                    score = new_score
                    my_move = move
                if score < beta:  # searching for the minimum
                    beta = score   # among the maximum scores
                if alpha >= beta:
                    break
                finish_time = time.time ()  # the timer stops
                elapsed_time = finish_time - self.start_time  # time spent in this move
                if elapsed_time > TIME_LIMIT:
                    break
            return my_move, score

    def find_all_correct_moves (self, board, my_color, op_color):
        board_size = len (board)
        correct_moves = []

        for row in range (board_size):
            for column in range (board_size):

                if board[row][column] == EMPTY_CELL:
                    move = (row, column)
                    if self.is_it_correct (board, move, my_color, op_color)[0]:
                        correct_moves.append (move)

        return correct_moves

    def is_it_correct (self, board, move, my_color, op_color):
        correct_directions = []
        cells_around = [(-1, -1), (-1, 0), (-1, 1),  # this array represents the coordinates
                        ( 0, -1),          ( 0, 1),      # of the cells around the given one
                        ( 1, -1), ( 1, 0), ( 1, 1)]

        for direction in cells_around:
            if self.confirm_direction (board, move, direction, my_color, op_color):
                correct_directions.append (direction)

        if correct_directions:
            return True, correct_directions
        return False, None

    def confirm_direction (self, board, move, direction, my_color, op_color):
        cell = [x + y for x, y in zip (move, direction)]  # cell = move + direction

        if self.cell_correctness (cell):
            if board[cell[0]][cell[1]] == op_color:
                while self.cell_correctness (cell):
                    cell = [x + y for x, y in zip (cell, direction)]

                    if self.cell_correctness (cell):
                        if board[cell[0]][cell[1]] == EMPTY_CELL:
                            return False
                        if board[cell[0]][cell[1]] == my_color:
                            return True
        return False

    def cell_correctness (self, cell):
        # checking whether the cell is located within the borders of the board
        if (LEFT_BORDER <= cell[0] <= RIGHT_BORDER) and (LEFT_BORDER <= cell[1] <= RIGHT_BORDER):
            return True
        return False

    def make_move (self, board, move, my_color, op_color):
        # replacing opponent's disks with mine

        correct_directions = self.is_it_correct (board, move, my_color, op_color)[1]
        cell = move
        board[cell[0]][cell[1]] = my_color

        for direction in correct_directions:
            cell = [x + y for x, y in zip (cell, direction)]  # cell = cell + direction

            while board[cell[0]][cell[1]] != my_color:
                board[cell[0]][cell[1]] = my_color
            cell = move
        return board

    def my_terminal_score (self, board):
        # calculating score for the selected move
        board_size = len (board)
        my_terminal_score = 0

        for row in range (board_size):
            for column in range (board_size):

                if board[row][column] == self.my_color:
                    my_terminal_score += self.get_score_for_the_move (row, column)

        return my_terminal_score

    def get_score_for_the_move (self, row, column):
        # returning score that can be got for this cell

        score_table = [[120, -20, 20,  5,  5, 20, -20, 120],
                       [-20, -40, -5, -5, -5, -5, -40, -20],
                       [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                       [  5,  -5,  3,  3,  3,  3,  -5,   5],
                       [  5,  -5,  3,  3,  3,  3,  -5,   5],
                       [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                       [-20, -40, -5, -5, -5, -5, -40, -20],
                       [120, -20, 20,  5,  5, 20, -20, 120]]

        return score_table[row][column]

