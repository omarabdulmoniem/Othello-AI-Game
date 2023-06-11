
import numpy as np

class Board:
    def __init__(self):
       self.size = 8
       self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]])

       self.board[3][3] = 1
       self.board[4][3] = -1
       self.board[3][4] = -1
       self.board[4][4] = 1
       self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]



    def get_size(self):
        return self.size

    def get_piece(self,row,column):
        return self.board[row][column]

    def set_piece(self,row,column,color):
        self.board[row][column] = color

    # Black = 1 and White = -1
    def is_valid(self,row,col,color):
        if self.board[row][col] != 0:
            return False

        # A loop to check every direction
        for x, y in self.directions:
            new_row = row + x
            new_col = col + y
            opponent_found = False

            # Move until you find empty, piece or edge
            while 0 <= new_row < self.size and 0 <= new_col < self.size:
                if self.board[new_row][new_col] == color:
                    if opponent_found:
                        return True
                    else:
                        break
                elif self.board[new_row][new_col] == 0:
                    break
                else:
                    opponent_found = True

                new_row += x
                new_col += y


        return False


    def get_valid_moves(self, color):
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid(row, col, color):
                    valid_moves.append((row, col))
        return valid_moves

    def flip_pieces_after_move(self, row, col, color):
        flipped_coins = self.get_flipped_coins(row, col, color)
        for coin in flipped_coins:
            self.board[coin[0]][coin[1]] = color

    def get_flipped_coins(self, row, col, color):
        flipped_coins = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dir_x, dir_y in directions:
            current_row, current_col = row + dir_x, col + dir_y
            coins_to_flip = []

            while 0 <= current_row < self.size and 0 <= current_col < self.size and\
                    self.board[current_row][current_col] != 'E':
                if self.board[current_row][current_col] == color:
                    flipped_coins.extend(coins_to_flip)
                    break
                else:
                    coins_to_flip.append((current_row, current_col))

                current_row += dir_x
                current_col += dir_y

        return flipped_coins

    # a method to flip pieces
    def flip(self, coins_to_flip, mycolor):
        for row, col in coins_to_flip:
            self.board[row][col] = -mycolor


    def count_pieces(self):
        black_count = 0
        white_count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 1:
                    black_count += 1
                elif self.board[row][col] == -1:
                    white_count += 1
        return black_count, white_count

