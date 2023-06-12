# from board_Modified import Board
import random
# import OthelloGame
from helper import Helper

class Ai:

    def __init__(self):
        self.helper = Helper()

    def get_best_move_Max(self, state, requiredDepth):
        empty_space = list(0 in row for row in state)
        if len(empty_space) == 1:
            valid_move = self.helper.get_valid_moves(1, state)
            return valid_move[0]

        best_eval = float('-inf')
        best_move = None
        for move in self.helper.get_valid_moves(1,state):
            state[move[0]][move[1]] = 1
            # print(state)
            state2 = self.helper.flip_pieces_after_move(move[0],move[1],1,state)
            eval = self.alphabeta(state2,0,requiredDepth,float('-inf'),float('inf'), False)
            state[move[0]][move[1]]  = 0
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def get_best_move_Min(self, state, requiredDepth):
        empty_space = list(0 in row for row in state)
        if len(empty_space) == 1:
            valid_move = self.helper.get_valid_moves(-1, state)
            return valid_move[0]
        best_eval = float('-inf')
        best_move = None
        for move in self.helper.get_valid_moves(-1, state):
            state[move[0]][move[1]] = 1
            state2 = self.helper.flip_pieces_after_move(move[0], move[1], -1, state)
            eval = self.alphabeta(state2, 0, requiredDepth, float('-inf'), float('inf'), True)
            state[move[0]][move[1]] = 0
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def alphabeta(self,state,depth,requiredDepth,alpha,beta,maximizer):
        result = self.evaluate()
        if depth >= requiredDepth:
            return result
        if(maximizer):
            max_eval = float('-inf')
            for move in self.helper.get_valid_moves(maximizer,state):
                state[move[0]][move[1]] = 1
                state2 = self.helper.flip_pieces_after_move(move[0], move[1], 1, state)
                eval = self.alphabeta(state2,depth + 1,requiredDepth,alpha,beta,False)
                state[move[0]][move[1]] = 0
                max_eval = max(max_eval,eval)
                alpha = max(alpha,max_eval)
                if(alpha >= beta):
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.helper.get_valid_moves(maximizer,state):
                state[move[0]][move[1]] = -1
                state2 = self.helper.flip_pieces_after_move(move[0], move[1], -1, state)
                eval = self.alphabeta(state2,depth + 1,requiredDepth,alpha, beta,True)
                state[move[0]][move[1]] = 0
                min_eval = min(min_eval, eval)
                alpha = min(alpha, min_eval)
                if (alpha >= beta):
                    break
            return min_eval


    #temporary function to heuristic function to test
    def evaluate(self):
        x = random.randint(0,9)
        # print(x)
        return x



#Ai = Ai()

#print(Ai.get_best_move_Min([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]], 4))

#game = OthelloGame.Othello()
#game.first_screen()


