import numpy as np

class Helper:

    def __init__(self):
        self.size = 8
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # Black = 1 and White = -1

    def get_valid_moves(self, player, board):
        valid_moves = []

        # Check each cell of the board
        for i in range(len(board)):
            for j in range(len(board[i])):
                # If the cell is empty, check if it's a valid move
                if board[i][j] == 0:
                    # Check in all eight directions
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue  # Skip the current cell

                            # Move in the current direction until a different player's piece is found or the edge of the board is reached
                            x, y = i + dx, j + dy
                            path = []  # Stores the path of opponent's pieces

                            while 0 <= x < len(board) and 0 <= y < len(board[x]):
                                if board[x][y] == -player:
                                    path.append((x, y))
                                    x += dx
                                    y += dy
                                elif board[x][y] == player and path:
                                    # If the next cell is the player's own piece and there is a path of opponent's pieces in between, it's a valid move
                                    valid_moves.append((i, j))
                                    break
                                else:
                                    break

        return valid_moves

    def flip_pieces_after_move(self, row, col, color, board_state):
        new_board_state = np.copy(board_state)
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