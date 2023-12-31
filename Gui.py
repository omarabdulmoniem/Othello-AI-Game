import tkinter
import turtle
from tkinter import *
SQUARE = 50
TILE = 20
BOARD_COLOR = 'brown'
LINE_COLOR = 'black'
TILE_COLORS = ['black', 'white']
MODE_OPTIONS = ["AI Vs AI", "Human Vs AI","Human Vs Human"]
LEVEL_OPTIONS = ["1","2","3","4","5"]


class Board:

    def __init__(self, n):
        self.n = n
        self.board = [[0] * n for i in range(n)]
        self.square_size = SQUARE
        self.board_color = BOARD_COLOR
        self.line_color = LINE_COLOR
        self.tile_size = TILE
        self.tile_colors = TILE_COLORS
        self.move = ()
        self.mode = ""
        self.level = ""

    def store_and_display_board(self):
        self.mode = self.clickedMode.get()
        self.level = self.clickedLevel.get()
        self.draw_board()
    def first_screen(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . centre')
        self.root.title("Othello Game")
        self.clickedMode = StringVar(self.root)
        self.clickedMode.set("Human Vs AI")
        self.root.geometry("500x500")
        label = Label(self.root, text="Welcome to Othello Game").pack(pady = 20)
        label = Label(self.root, text="Mode:").pack(padx=20, pady=15, side=tkinter.LEFT)
        dropDownMenuMode = OptionMenu(self.root,self.clickedMode,*MODE_OPTIONS).pack(padx=10, pady=15, side=tkinter.LEFT)

        self.clickedLevel = StringVar(self.root)
        self.clickedLevel.set("1")
        label = Label(  self.root, text="Level:").pack(padx=20, pady=15, side=tkinter.LEFT)
        dropDownMenuLevel = OptionMenu(  self.root,self.clickedLevel,*LEVEL_OPTIONS).pack(padx=10, pady=15, side=tkinter.LEFT)


        button = Button(  self.root, text="Play", command=self.store_and_display_board).pack(padx=10, pady=15, side=tkinter.LEFT)
        self.root.mainloop()

    def draw_board(self):
        # self.root.destroy()
        turtle.setup(self.n * self.square_size + self.square_size,
                     self.n * self.square_size + self.square_size)
        turtle.screensize(self.n * self.square_size, self.n * self.square_size)
        turtle.bgcolor('white')

        # Create the turtle to draw the board
        othello = turtle.Turtle(visible=False)
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

        # Set line color and fill color
        othello.color(self.line_color, self.board_color)

        # Move the turtle to the upper left corner
        corner = -self.n * self.square_size / 2
        othello.setposition(corner, corner)

        # Draw the board background
        othello.begin_fill()
        for i in range(4):
            othello.pendown()
            othello.forward(self.square_size * self.n)
            othello.left(90)
        othello.end_fill()

        # Draw the horizontal lines
        for i in range(self.n + 1):
            othello.setposition(corner, self.square_size * i + corner)
            self.draw_lines(othello)

        # Draw the vertical lines
        othello.left(90)
        for i in range(self.n + 1):
            othello.setposition(self.square_size * i + corner, corner)
            self.draw_lines(othello)
        self.initialize_board()
        self.run()

    def draw_lines(self, turt):

        turt.pendown()
        turt.forward(self.square_size * self.n)
        turt.penup()

    def is_on_board(self, x, y):
        bound = self.n / 2 * self.square_size

        if - bound < x < bound and - bound < y < bound:
            return True
        return False

    def is_on_line(self, x, y):
        if self.is_on_board(x, y):
            if x % self.square_size == 0 or y % self.square_size == 0:
                return True
        return False

    def convert_coord(self, x, y):
        if self.is_on_board(x, y):
            row = int(self.n / 2 - 1 - y // self.square_size)
            col = int(self.n / 2 + x // self.square_size)
            return (row, col)
        return ()

    def get_coord(self, x, y):
        if self.is_on_board(x, y) and not self.is_on_line(x, y):
            self.move = self.convert_coord(x, y)
        else:
            self.move = ()

    def get_tile_start_pos(self, square):
        if square == ():
            return ()

        for i in range(2):
            if square[i] not in range(self.n):
                return ()

        row, col = square[0], square[1]

        y = ((self.n - 1) / 2 - row) * self.square_size
        if col < self.n / 2:
            x = (col - (self.n - 1) / 2) * self.square_size - self.tile_size
            r = - self.tile_size
        else:
            x = (col - (self.n - 1) / 2) * self.square_size + self.tile_size
            r = self.tile_size

        return ((x, y), r)

    def draw_tile(self, square, color):
        # Get starting position and radius of the tile
        pos = self.get_tile_start_pos(square)
        if pos:
            coord = pos[0]
            r = pos[1]
        else:
            print('Error drawing the tile...')
            return

        # Create the turtle to draw the tile
        tile = turtle.Turtle(visible=False)
        tile.penup()
        tile.speed(0)
        tile.hideturtle()

        # Set color of the tile
        tile.color(self.tile_colors[color])

        # Move the turtle to the starting postion for drawing
        tile.setposition(coord)
        tile.setheading(90)

        # Draw the tile
        tile.begin_fill()
        tile.pendown()
        tile.circle(r)
        tile.end_fill()

    def __str__(self):
        explanation = 'State of the board:\n'
        board_str = ''
        for row in self.board:
            board_str += str(row) + '\n'
        printable_str = explanation + board_str

        return printable_str

    def __eq__(self, other):
        return self.board == other.board