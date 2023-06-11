import turtle
from Gui import Board
class Othello(Board):
    def __init__(self, n = 8):

        Board.__init__(self, n)
        self.current_player = 0
        self.num_tiles = [2, 2]
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
            self.board[row][col] = color + 1
            self.draw_tile(initial_squares[i], color)
        turtle.speed(0)
        turtle.shape("square")
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(-200, 200)
        turtle.write("Score Black:",align="left", font=("Ariel", 10, "bold"))
        turtle.goto(0, 200)
        turtle.write("Score White:", align="left", font=("Ariel", 10, "bold"))

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
        turtle.onscreenclick(self.play)
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
        self.board[self.move[0]][self.move[1]] = self.current_player + 1
        self.num_tiles[self.current_player] += 1
        self.draw_tile(self.move, self.current_player)

    def play(self, x, y):
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
        self.get_coord(x, y)
        turtle.onscreenclick(None)
        self.make_move()
        # Play the user's turn
        # if self.has_legal_move():
        #     self.get_coord(x, y)
        #     if self.is_legal_move(self.move):
        #         turtle.onscreenclick(None)
        #         self.make_move()
        #     else:
        #         return

        # # Play the computer's turn
        # while True:
        #     self.current_player = 1
        #     if self.has_legal_move():
        #         print('Computer\'s turn.')
        #         self.make_random_move()
        #         self.current_player = 0
        #         if self.has_legal_move():
        #             break
        #     else:
        #         break

        # # Switch back to the user's turn
        # self.current_player = 0

        # # Check whether the game is over
        # if not self.has_legal_move() or sum(self.num_tiles) == self.n ** 2:
        #     turtle.onscreenclick(None)
        #     print('-----------')
        #     self.report_result()
        #     name = input('Enter your name for posterity\n')
        #     # if not score.update_scores(name, self.num_tiles[0]):
        #     #     print('Your score has not been saved.')
        #     print('Thanks for playing Othello!')
        #     close = input('Close the game screen? Y/N\n')
        #     if close == 'Y':
        #         turtle.bye()
        #     elif close != 'N':
        #         print('Quit in 3s...')
        #         turtle.ontimer(turtle.bye, 3000)
        # else:
        #     print('Your turn.')
        #     turtle.onscreenclick(self.play)
