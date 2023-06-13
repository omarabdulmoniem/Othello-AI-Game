# Othello Game

A simple Python-based version of [Othello game](https://en.wikipedia.org/wiki/Reversi) built with the [turtle library](https://docs.python.org/3.7/library/turtle.html).
Here's a gif below showing how to use our GUI to play Othello :)

<img src="AI_Project_AdobeExpress.gif" width="500" height="500"/>


## Instructions

Start: `python main.py` (python3 is required for playing the game)

The game is played with black-and-white tiles on an 8x8 board. The object of the game is to have more tiles of your color than your computer opponent has of its. 

- Play begins with 4 tiles in the middle: two white and two black. The user plays the black tile while the computer plays the white tile.
- Black goes first. That player lays down a tile, which must be in a legal position. Any white tiles in between the new black tile and an existing black tile get flipped.
- Play continues, with the players taking turns until the whole board is covered or there are no more legal moves.
- When the board is completely covered in tiles, or there are no more legal moves, then the game is over. Whichever player has more tiles of their color on the board wins. The program will announce the winner and how many tiles they have on the board. Ties can happen, too.
- Our GUI has 3 modes 'Human vs Human', 'AI vs Human' and 'AI vs AI' for each mode you can select the difficulty from 1-5.  


**Legal moves**: for a move to be legal, a tile must be placed such that at least one opposing tile will be flipped.

## File structure

- `AI.py`: contains a class that handles Alphabeta best moves.
- `board.py`: contains a class that represents the game board.
- `helper.py`: contains a class that used across different classes to determine the valid moves.
- `main.py`: the main entry port for the game.
- `OthelloGame.py`: contains a class that represents the game logic.

## Disclaimer

This is a project for *CSE472 Artifitial Intelligence of Computer and Systems Engineering*.
