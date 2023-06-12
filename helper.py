import numpy as np

class Helper:

    def __init__(self):
        self.size = 8
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # Black = 1 and White = -1
    def is_valid(self, row, col, color, board_state):
        if board_state[row][col] != 0:
            return False

        # A loop to check every direction
        for x, y in self.directions:
            new_row = row + x
            new_col = col + y
            opponent_found = False

            # Move until you find empty, piece or edge
            while 0 <= new_row < self.size and 0 <= new_col < self.size:
                if board_state[new_row][new_col] == color:
                    if opponent_found:
                        return True
                    else:
                        break
                elif board_state[new_row][new_col] == 0:
                    break
                else:
                    opponent_found = True

                new_row += x
                new_col += y

        return False

    def get_valid_moves(self, color, board_state):
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid(row, col, color, board_state):
                    valid_moves.append((row, col))
        return valid_moves

    def flip_pieces_after_move(self, row, col, color, board_state):
        new_board_state = board_state
        flipped_coins = self.get_flipped_coins(row, col, color, new_board_state)
        for coin in flipped_coins:
            new_board_state[coin[0]][coin[1]] = color

        return new_board_state

    def get_flipped_coins(self, row, col, color, board_state):
        flipped_coins = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dir_x, dir_y in directions:
            current_row, current_col = row + dir_x, col + dir_y
            coins_to_flip = []

            while 0 <= current_row < self.size and 0 <= current_col < self.size and \
                board_state[current_row][current_col] != '0':
                if board_state[current_row][current_col] == color:
                    flipped_coins.extend(coins_to_flip)
                    break
                else:
                    coins_to_flip.append((current_row, current_col))

                current_row += dir_x
                current_col += dir_y

        return flipped_coins