import turtle
from Gui import Board
from helper import Helper
from Ai import Ai
from tkinter import messagebox
class Othello(Board):
    def __init__(self, n = 8):
        self.Ai = Ai()
        self.helper = Helper()
        Board.__init__(self, n)
        self.current_player = 0
        self.num_tiles = [2, 2]
        self.playFlag = False
        self.player = 1
        self.humanflag = 0


    def initialize_board(self):
        if self.n < 2:
            return

        coord1 = int(self.n / 2 - 1)
        coord2 = int(self.n / 2)
        initial_squares = [(coord1, coord2), (coord1, coord1),
                           (coord2, coord1), (coord2, coord2)]

        for i in range(len(initial_squares)):
            color = i % 2
            row = initial_squares[i][0]
            col = initial_squares[i][1]
            if color == 1:
                self.board[row][col] = -1
            elif color == 0:
                self.board[row][col] = 1
            # self.board[row][col] = color + 1
            self.draw_tile(initial_squares[i], color)

            turtle.speed(0)
            turtle.shape("square")
            turtle.penup()
            turtle.hideturtle()
            white = "Score White: " + str(0)
            black = "Score Black: " + str(0)
            turtle.goto(-200, 200)
            turtle.write(white, align="left", font=("Ariel", 12))
            turtle.goto(0, 200)
            turtle.write(white, align="left", font=("Ariel", 12))

    def update_score(self):
        whiteScore = 0;
        blackScore = 0;
        for i in range(len(self.board)):
            for j in self.board[i]:
                if j == -1:
                    whiteScore+=1;
                elif j == 1:
                    blackScore+=1;
        turtle.speed(0)
        turtle.shape("square")
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(-200, 200)
        turtle.clear()
        white = "Score White: "+ str(whiteScore)
        black = "Score Black: " + str(blackScore)
        turtle.write(black, align="left", font=("Ariel", 12))
        turtle.goto(0, 200)
        #turtle.clear()
        turtle.write(white, align="left", font=("Ariel", 12))

    def run(self):
        ''' Method: run
            Parameters: self
            Returns: nothing
            Does: Starts the game, sets the user to be the first player,
                  and then alternate back and forth between the user and
                  the computer until the game is over.
        '''
        if self.current_player not in (0, 1):
            print('Error: unknown player. Quit...')
            return

        self.current_player = 0
        print('Your turn.')
        if (self.mode == "Human Vs AI"):
            turtle.onscreenclick(self.play_human_ai)
            turtle.mainloop()
        elif (self.mode == "AI Vs AI"):
            self.play_ai_ai()
            turtle.mainloop()
        elif (self.mode == "Human Vs Human"):
            turtle.onscreenclick(self.play_human_human)
            turtle.mainloop()

    def make_move(self):
        ''' Method: make_move
            Parameters: self
            Returns: nothing
            Does: Draws a tile for the player's next legal move on the
                  board and flips the adversary's tiles. Also, updates the
                  state of the board (1 for black tiles and 2 for white
                  tiles), and increases the number of tiles of the current
                  player by 1.
        '''
        # if self.is_legal_move(self.move):
        # self.board[self.move[0]][self.move[1]] = self.current_player + 1
        if self.current_player == 0:
            self.board[self.move[0]][self.move[1]] = 1
        elif self.current_player == 1:
            print(self.move)
            self.board[self.move[0]][self.move[1]] = -1
        player = -1 if self.current_player else 1
        flipped = self.helper.get_flipped_coins(self.move[0], self.move[1], player, self.board)
        print("Flipped coins: ", flipped)
        self.draw_tile(self.move, self.current_player)
        self.num_tiles[self.current_player] += 1
        for tile in flipped:
            self.draw_tile(tile, self.current_player)
            self.board[tile[0]][tile[1]] = player
        self.update_score()
        self.who_play()

    def win_lose_game(self):
        white = 0
        black = 0
        win = 0
        empty = 0
        for i in range(len(self.board)):
            for j in self.board[i]:
                if j == -1:
                    white += 1
                elif j == 1:
                    black += 1
                else:
                    empty += 1
        if (white == 64 or black == 64):
            win = 1

        if (len(self.helper.get_valid_moves(-1, self.board)) == 0 and len(self.helper.get_valid_moves(1,
                                                                                                      self.board)) == 0) or win or empty == 0:
            return False
        return True

    def check_game_over(self, board):
        has_empty_space = any(0 in row for row in board)

        # Check if there are valid moves for both players
        black_has_valid_moves = any(self.helper.get_valid_moves(1, board))
        white_has_valid_moves = any(self.helper.get_valid_moves(-1, board))

        if not has_empty_space or (not black_has_valid_moves and not white_has_valid_moves):
            return False

        return True

    def who_play(self):
        if (self.current_player == 1):
            turtle.speed(0)
            turtle.shape("square")
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(-200, 180)
            white = "White turn : " + str(0)
            turtle.write(white, align="left", font=("Ariel", 10, "bold"))
            turtle.goto(-0, 180)
            black = "Black turn: " + str(1)
            turtle.write(black, align="left", font=("Ariel", 10, "bold"))
        elif (self.current_player == 0):
            turtle.speed(0)
            turtle.shape("square")
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(-200, 180)
            white = "White turn : " + str(1)
            turtle.write(white, align="left", font=("Ariel", 10, "bold"))
            turtle.goto(-0, 180)
            black = "Black turn : 0" + str(0)
            turtle.write(black, align="left", font=("Ariel", 10, "bold"))

    def play_human_ai(self, x, y):
        ''' Method: play
            Parameters: self, x (float), y (float)
            Returns: nothing
            Does: Plays alternately between the user's turn and the computer's
                  turn. The user plays the first turn. For the user's turn,
                  gets the user's move by their click on the screen, and makes
                  the move if it is legal; otherwise, waits indefinitely for a
                  legal move to make. For the computer's turn, just makes a
                  random legal move. If one of the two players (user/computer)
                  does not have a legal move, switches to another player's
                  turn. When both of them have no more legal moves or the
                  board is full, reports the result, saves the user's score
                  and ends the game.

                  About the input: (x, y) are the coordinates of where
                  the user clicks.
        '''

        player = -1 if self.current_player else 1

        # Play the user's turn

        if len(self.helper.get_valid_moves(player, self.board)):
            self.get_coord(x, y)
            turtle.onscreenclick(None)
            if (self.move[0], self.move[1]) in self.helper.get_valid_moves(player, self.board):
                turtle.onscreenclick(None)
                self.make_move()
                self.playFlag = True
            else:
                self.playFlag = False

        # Play the computer's turn
        while self.playFlag:
            self.current_player = 1
            if len(self.helper.get_valid_moves(-1, self.board)):
                print('Computer\'s turn.')
                print(self.helper.get_valid_moves(-1, self.board))
                self.move = self.Ai.get_best_move_Min(self.board, int(self.level) + 2)
                turtle.onscreenclick(None)
                print(self.move)
                self.make_move()

                self.current_player = 0
                if len(self.helper.get_valid_moves(-1, self.board)):
                    break
            else:
                break

        player = -1 if self.current_player else 1

        # Check whether the game is over
        if not self.win_lose_game():
            turtle.onscreenclick(None)
            print('-----------')
        else:
            print('Your turn.')
            turtle.onscreenclick(self.play_human_ai)

    def play_ai_ai(self):
        while self.win_lose_game():
            while True:
                self.current_player = 0
                if len(self.helper.get_valid_moves(1, self.board)):
                    print('First Computer\'s turn.')
                    print(self.helper.get_valid_moves(1, self.board))
                    self.move = self.Ai.get_best_move_Max(self.board, 2)
                    turtle.onscreenclick(None)
                    print(self.move)

                    if self.move != None:
                        self.make_move()
                    else:
                        break

                    self.current_player = 1
                    if len(self.helper.get_valid_moves(1, self.board)):
                        break
                else:
                    break

            while True:
                self.current_player = 1
                if len(self.helper.get_valid_moves(-1, self.board)):
                    print('Second Computer\'s turn.')
                    print(self.helper.get_valid_moves(-1, self.board))
                    self.move = self.Ai.get_best_move_Min(self.board, 2)
                    turtle.onscreenclick(None)
                    print(self.move)
                    if self.move != None:
                        self.make_move()
                    else:
                        break

                    self.current_player = 0
                    if len(self.helper.get_valid_moves(-1, self.board)):
                        break
                else:
                    break


        if self.num_tiles[0] > self.num_tiles[1]:
            messagebox.showinfo("Message","Black wins!!!!")
        else:
            messagebox.showinfo("Message","White wins!!!!")


    def play_human_human(self,x,y):
        if len(self.helper.get_valid_moves(self.player, self.board)):
            self.get_coord(x, y)
            turtle.onscreenclick(None)
            if (self.move[0], self.move[1]) in self.helper.get_valid_moves(self.player, self.board):
                turtle.onscreenclick(None)
                self.make_move()
                self.humanflag = 1

        if self.humanflag == 1:
            self.humanflag = 0
            if self.current_player == 0:
                self.current_player = 1;
            else:
                self.current_player = 0;
            self.player = self.player * (-1)
        if(self.win_lose_game()):
            turtle.onscreenclick(self.play_human_human)
        else:
            if self.num_tiles[0] > self.num_tiles[1]:
                messagebox.showinfo("Message","Black wins!!!!")
            else:
                messagebox.showinfo("Message","White wins!!!!")

