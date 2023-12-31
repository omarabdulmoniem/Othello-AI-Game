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
        self.black_num = 0
        self.white_num = 0


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
            turtle.write(black, align="left", font=("Ariel", 12))
            turtle.goto(-75, 200)
            turtle.write(white, align="left", font=("Ariel", 12))
            turtle.goto(70, 200)
            turtle.write("Black turn", align="left", font=("Ariel", 10, "bold"))

    def update_score(self):
        whiteScore = 0;
        blackScore = 0;
        for i in range(len(self.board)):
            for j in self.board[i]:
                if j == -1:
                    whiteScore+=1;
                elif j == 1:
                    blackScore+=1;
        print("Score Black: " + str(blackScore))
        print("Score White: " + str(whiteScore))
        self.black_num = blackScore
        self.white_num = whiteScore
        turtle.speed(0)
        turtle.shape("square")
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(-200, 200)
        turtle.clear()
        white = "Score White: "+ str(whiteScore)
        black = "Score Black: " + str(blackScore)
        turtle.write(black, align="left", font=("Ariel", 12))
        turtle.goto(-75, 200)
        #turtle.clear()
        turtle.write(white, align="left", font=("Ariel", 12))
        turtle.goto(70, 200)
        if (self.current_player == 1):
            turtle.write("Black turn", align="left", font=("Ariel", 12))
        else:
            turtle.write("white turn", align="left", font=("Ariel", 12))
    def run(self):

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


    def play_human_ai(self, x, y):

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
        else:
            self.playFlag = True

        # Play the computer's turn
        while self.playFlag:
            self.current_player = 1
            if len(self.helper.get_valid_moves(-1, self.board)):
                print('Computer\'s turn.')
                print(self.helper.get_valid_moves(-1, self.board))
                self.move = self.Ai.get_best_move_Min(self.board, int(self.level) + 2)
                if self.move == None:
                    break
                turtle.onscreenclick(None)
                print(self.move)
                self.make_move()

                self.current_player = 0
                if len(self.helper.get_valid_moves(-1, self.board)):
                    break
            else:
                self.current_player = 0
                break

        player = -1 if self.current_player else 1

        # Check whether the game is over
        if not self.win_lose_game():
            turtle.onscreenclick(None)
            print('-----------')
            if self.black_num > self.white_num:
                print(self.num_tiles)
                messagebox.showinfo("Message", "Black wins!")
            else:
                print(self.num_tiles)
                messagebox.showinfo("Message", "White wins!")
        else:
            print('Your turn.')
            print("Valid Moves: ")
            print(self.helper.get_valid_moves(player, self.board))
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


        if self.black_num > self.white_num:
            print(self.num_tiles)
            messagebox.showinfo("Message","Black wins!!!!")
        else:
            print(self.num_tiles)
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
                print(self.num_tiles)
                messagebox.showinfo("Message","Black wins!")
            else:
                print(self.num_tiles)
                messagebox.showinfo("Message","White wins!")

