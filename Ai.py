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
        result = self.heuristic_value(state)
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

    def heuristic_value(self, array):

        # coin parity
        Max_Player_Coins = 0
        Min_Player_Coins = 0
        for i in range(8):
            for j in range(8):
                if array[i][j] == 1:
                    Max_Player_Coins = Max_Player_Coins + 1
                elif array[i][j] == -1:
                    Min_Player_Coins = Min_Player_Coins + 1
                else:
                    continue
        # print("Max Player Coins:",Max_Player_Coins)
        # print("Min Player Coins:",Min_Player_Coins)
        Coin_Parity_Heuristic_Value = (
                100 * (Max_Player_Coins - Min_Player_Coins) / (Max_Player_Coins + Min_Player_Coins))
        # print("Coin Parity Heuristic Value:",Coin_Parity_Heuristic_Value)
        # print('Hello world')
        # Mobility
        # Actual Mobility Value
        Max_Player_Actual_Mobility_Value = 0
        Min_Player_Actual_Mobility_Value = 0

        for i in range(8):
            for j in range(8):
                if array[i][j] == 1:
                  if j!=7:
                    if array[i][j + 1] == -1:
                        for z in range(8 - j - 1):
                            if array[i][j + 2 + z] == 0:
                                Max_Player_Actual_Mobility_Value = Max_Player_Actual_Mobility_Value + 1
                                break

                    if (j != 0) and (j != 1):
                        if array[i][j - 1] == -1:
                            for z in range(j - 1):
                                if array[i][j - 2 - z] == 0:
                                    Max_Player_Actual_Mobility_Value = Max_Player_Actual_Mobility_Value + 1
                                    break

                    if array[i + 1][j] == -1:
                        # if array[i+1][j] == -1:
                        for z in range(i + 2, 6):
                            if array[i][z] == 0:
                                Max_Player_Actual_Mobility_Value = Max_Player_Actual_Mobility_Value + 1
                                break

                    if (i != 0) and (i != 1):
                        if array[i - 1][j] == -1:
                            for z in range(i):
                                if array[i - 2 - z][j] == 0:
                                    Max_Player_Actual_Mobility_Value = Max_Player_Actual_Mobility_Value + 1
                                    break
        # print("Max_Player_Actual_Mobility_Value:" )
        # print(Max_Player_Actual_Mobility_Value)

        for i in range(8):
            for j in range(8):
                if array[i][j] == -1:
                    if array[i][j + 1] == 1:
                        for z in range(8 - j - 1):
                         if j+2+z <8:
                            if array[i][j + 2 + z] == 0:
                                Min_Player_Actual_Mobility_Value = Min_Player_Actual_Mobility_Value + 1
                                break

                    if (j != 0) and (j != 1):
                        if array[i][j - 1] == 1:
                            for z in range(j - 1):
                                if array[i][j - 2 - z] == 0:
                                    Min_Player_Actual_Mobility_Value = Min_Player_Actual_Mobility_Value + 1
                                    break

                    if array[i + 1][j] == 1:
                        # if array[i+1][j] == -1:
                        for z in range(i + 2, 6):
                            if array[i][z] == 0:
                                Min_Player_Actual_Mobility_Value = Min_Player_Actual_Mobility_Value + 1
                                break

                    if (i != 0) and (i != 1):
                        if array[i - 1][j] == 1:
                            for z in range(i):
                                if array[i - 2 - z][j] == 0:
                                    Min_Player_Actual_Mobility_Value = Min_Player_Actual_Mobility_Value + 1
                                    break
        # print("Coin Parity Heuristic Value:",Coin_Parity_Heuristic_Value)
        # print("Min_Player_Actual_Mobility_Value:")
        # print(Min_Player_Actual_Mobility_Value)

        # potential mobility
        Max_Player_Potential_Mobility_Value = 0
        Min_Player_Potential_Mobility_Value = 0

        for i in range(8):
            for j in range(8):
                if array[i][j] == -1:
                    if array[i][j + 1] == 0:
                        Max_Player_Potential_Mobility_Value = Max_Player_Potential_Mobility_Value + 1
                    if (j != 0) and (j != 1):
                        if array[i][j - 1] == 0:
                            Max_Player_Potential_Mobility_Value = Max_Player_Potential_Mobility_Value + 1

                    if array[i + 1][j] == 0:
                        Max_Player_Potential_Mobility_Value = Max_Player_Potential_Mobility_Value + 1

                    if (i != 0) and (i != 1):
                        if array[i - 1][j] == 0:
                            Max_Player_Potential_Mobility_Value = Max_Player_Potential_Mobility_Value + 1
        # print("Max_Player_potential_Mobility_Value:")
        # print(Max_Player_Potential_Mobility_Value)

        # for min player
        # if array[i][j]== -1:
        for i in range(8):
            for j in range(8):
                if array[i][j] == 1:
                 if j!=7:
                    if array[i][j + 1] == 0:
                        Min_Player_Potential_Mobility_Value = Min_Player_Potential_Mobility_Value + 1
                    if (j != 0) and (j != 1):
                        if array[i][j - 1] == 0:
                            Min_Player_Potential_Mobility_Value = Min_Player_Potential_Mobility_Value + 1

                    if array[i + 1][j] == 0:
                        Min_Player_Potential_Mobility_Value = Min_Player_Potential_Mobility_Value + 1

                    if (i != 0) and (i != 1):
                        if array[i - 1][j] == 0:
                            Min_Player_Potential_Mobility_Value = Min_Player_Potential_Mobility_Value + 1
        # print("Min_Player_potential_Mobility_Value:")
        # print(Min_Player_Potential_Mobility_Value)
        Actual_Mobility_Heuristic_Value = 0
        Potential_Mobility_Heuristic_Value = 0

        if ((Max_Player_Actual_Mobility_Value + Min_Player_Actual_Mobility_Value) != 0):
            Actual_Mobility_Heuristic_Value = 100 * (
                    Max_Player_Actual_Mobility_Value - Min_Player_Actual_Mobility_Value) / (
                                                      Max_Player_Actual_Mobility_Value + Min_Player_Actual_Mobility_Value)
        else:
            Actual_Mobility_Heuristic_Value = 0
        # print("Actual_Mobility_Heuristic_Value:")
        # print(Actual_Mobility_Heuristic_Value)

        if ((Max_Player_Potential_Mobility_Value + Min_Player_Potential_Mobility_Value) != 0):
            Potential_Mobility_Heuristic_Value = 100 * (
                    Max_Player_Potential_Mobility_Value - Min_Player_Potential_Mobility_Value) / (
                                                         Max_Player_Potential_Mobility_Value + Min_Player_Potential_Mobility_Value)
        else:
            Potential_Mobility_Heuristic_Value = 0
        # print("potential_Mobility_Heuristic_Value:")
        # print(Potential_Mobility_Heuristic_Value)
        Mobility_value = Actual_Mobility_Heuristic_Value + Potential_Mobility_Heuristic_Value
        # print("Mobility_value:", Mobility_value)

        # Corners Captured
        Potential_corner = 0
        unlikely_corner = 0
        Max_captured_corners = 0
        Min_captured_corners = 0

        # from maximum(black) point of view
        up_left_corner = 0
        if array[0][0] == 1:
            Max_captured_corners = Max_captured_corners + 1
            # print("array 0 w 0b 1")
        elif array[0][0] == 0:
            # print("array 0 w 0b 0")
            for j in range(6):
                if array[0][j + 1] == -1:
                    continue
                elif array[0][j + 2] == 1:
                    Potential_corner = Potential_corner + 1
                    up_left_corner = 1
                else:
                    break
                    # vertically
            if up_left_corner == 0:
                for i in range(6):
                    if array[i + 1][0] == -1:
                        continue
                    elif array[0][i + 2] == 1:
                        Potential_corner = Potential_corner + 1
                        up_left_corner = 1
                    else:
                        break
                        # diagonally
            if up_left_corner == 0:
                for i in range(6):
                    if array[i + 1][i + 1] == -1:
                        continue
                    elif array[i + 2][i + 2] == 1:
                        Potential_corner = Potential_corner + 1
                        up_left_corner = 1

                    else:
                        break
        # print("Potential_corner after first",Potential_corner)
        up_right_corner = 0
        if array[0][7] == 1:
            Max_captured_corners = Max_captured_corners + 1
            # print("array 0 w 7 b 1")
        elif array[0][7] == 0:
            # print("array 0 w 7 b 0")
            # vertically
            for i in range(6):
                if array[i + 1][7] == -1:
                    continue
                elif array[i + 2][7] == 1:
                    Potential_corner = Potential_corner + 1
                    up_right_corner = 1

                else:
                    break
                # horizontally
            if up_right_corner == 0:
                for i in range(6):
                    if array[0][6 - i] == -1:
                        continue
                    elif array[0][5 - i] == 1:
                        Potential_corner = Potential_corner + 1
                        up_right_corner = 1
                    else:
                        break
            if up_right_corner == 0:
                # diagonally
                for i in range(6):
                    if array[i + 1][6 - i] == -1:
                        continue
                    elif array[i + 2][5 - i] == 1:
                        Potential_corner = Potential_corner + 1
                        up_right_corner = 1

                    else:
                        break
        # print("Potential_corner after second",Potential_corner)
        bottom_left_corner = 0
        if array[7][0] == 1:
            # print("array7 0 b 1")
            Max_captured_corners = Max_captured_corners + 1
        elif array[7][0] == 0:
            # print("array7 0 b 0")

            # horizontally
            for i in range(6):
                if array[7][i + 1] == -1:
                    continue
                elif array[7][i + 2] == 1:
                    Potential_corner = Potential_corner + 1
                    bottom_left_corner = 1

                else:
                    break
            if bottom_left_corner == 0:
                for i in range(5):
                    if array[6 - i][0] == -1:
                        continue
                    elif array[5 - i][0] == 1:
                        Potential_corner = Potential_corner + 1
                        bottom_left_corner = 1
                    else:
                        break
                        # diagonally
            if bottom_left_corner == 0:
                for i in range(6):
                    if array[6 - i][i + 1] == -1:
                        continue
                    elif array[5 - i][2 + i] == 1:
                        Potential_corner = Potential_corner + 1
                        bottom_left_corner = 1
                    else:
                        break
        bottom_right_corner = 0
        if array[7][7] == 1:
            Max_captured_corners = Max_captured_corners + 1
            # print("array 7 7 one")
        elif array[7][7] == 0:
            # horizontally
            # print("array 7 7 zero")
            for i in range(6):
                if array[7][5 - i + 1] == -1:
                    continue
                elif array[7][5 - i] == 1:
                    Potential_corner = Potential_corner + 1
                    bottom_right_corner = 1

                else:
                    break
                    # vertically
            if bottom_right_corner == 0:
                for i in range(6):
                    if array[5 - i + 1][7] == -1:
                        continue
                    elif array[5 - i][7] == 1:
                        Potential_corner = Potential_corner + 1
                        bottom_right_corner = 1
                    else:
                        break
            if bottom_right_corner == 0:
                # diagonally
                for i in range(5):
                    if array[6 - i][6 - i] == -1:
                        continue
                    elif array[5 - i][5 - i] == 1:
                        Potential_corner = Potential_corner + 1
                        bottom_right_corner == 1
                    else:
                        break
        # print("Max_captured_corners:")
        # print(Max_captured_corners)
        # print("Max_Potential_corner:")
        # print(Potential_corner)

        # from minimum(white) point of view
        Min_Potential_corner = 0
        min_up_left = 0
        if array[0][0] == -1:
            Min_captured_corners = Min_captured_corners + 1
        elif array[0][0] == 0:
            for j in range(6):
                if array[0][j + 1] == -1:
                    continue
                elif array[0][j + 2] == 1:
                    Min_Potential_corner = Potential_corner + 1
                    min_up_left = 1
                else:
                    break
                    # vertically
            if min_up_left == 0:
                for i in range(6):
                    if array[i + 1][0] == -1:
                        continue
                    elif array[0][i + 2] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_up_left = 1
                    else:
                        break
                        # diagonally
            if min_up_left == 0:
                for i in range(6):
                    if array[i + 1][i + 1] == -1:
                        continue
                    elif array[i + 2][i + 2] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_up_left = 1
                    else:
                        break
        min_up_right = 0
        if array[0][7] == -1:
            Min_captured_corners = Min_captured_corners + 1
        elif array[0][7] == 0:
            # vertically
            for i in range(6):
                if array[i + 1][7] == -1:
                    continue
                elif array[i + 2][7] == 1:
                    Min_Potential_corner = Potential_corner + 1
                    min_up_right = 1
                else:
                    break
                # horizontally
            if min_up_right == 0:
                for i in range(6):
                    if array[0][6 - i] == -1:
                        continue
                    elif array[0][5 - i] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_up_right = 1
                    else:
                        break
                    # diagonally
            if min_up_right == 0:
                for i in range(6):
                    if array[i + 1][6 - i] == -1:
                        continue
                    elif array[i + 2][5 - i] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_up_right = 1
                    else:
                        break
        min_bottom_left = 0
        if array[7][0] == -1:
            Min_captured_corners = Min_captured_corners + 1
        elif array[7][0] == 0:
            # horizontally
            for i in range(6):
                if array[7][i + 1] == -1:
                    continue
                elif array[7][i + 2] == 1:
                    Min_Potential_corner = Potential_corner + 1
                    min_bottom_left = 1
                else:
                    break
                    # vertically
            if min_bottom_left == 0:
                for i in range(5):
                    if array[6 - i][0] == -1:
                        continue
                    elif array[5 - i][0] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_bottom_left = 1
                    else:
                        break
                        # diagonally
            if min_bottom_left == 0:
                for i in range(6):
                    if array[6 - i][i + 1] == -1:
                        continue
                    elif array[5 - i][2 + i] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_bottom_left = 1
                    else:
                        break
        min_bottom_right = 0
        if array[7][7] == -1:
            Min_captured_corners = Min_captured_corners + 1
        elif array[7][7] == 0:
            # horizontally
            for i in range(6):
                if array[7][5 - i + 1] == -1:
                    continue
                elif array[7][5 - i] == 1:
                    Min_Potential_corner = Potential_corner + 1
                    min_bottom_right = 1
                else:
                    break
                    # vertically
            if min_bottom_right == 0:
                for i in range(6):
                    if array[5 - i + 1][7] == -1:
                        continue
                    elif array[5 - i][7] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_bottom_right = 1
                    else:
                        break
                        # diagonally
            if min_bottom_right == 0:
                for i in range(5):
                    if array[6 - i][6 - i] == -1:
                        continue
                    elif array[5 - i][5 - i] == 1:
                        Min_Potential_corner = Potential_corner + 1
                        min_bottom_right = 1
                    else:
                        break
        # print("Min_captured_corners:")
        # print(Min_captured_corners)
        # print("Min Potential_corner:")
        # print(Min_Potential_corner)
        # assume weights 50%captured corners 25% potential 25% unlikely

        Max_Player_Corner_Value = (0.5 * Max_captured_corners) + (0.25 * Potential_corner) + (0.25 * 0)
        Min_Player_Corner_Value = (0.5 * Min_captured_corners) + (0.25 * Min_Potential_corner) + (0.25 * 0)
        # print("Max_Player_Corner_Value",Max_Player_Corner_Value )
        # print("Min_Player_Corner_Value",Min_Player_Corner_Value)
        if ((Max_Player_Corner_Value + Min_Player_Corner_Value) != 0):
            Corner_Heuristic_Value = 100 * (Max_Player_Corner_Value - Min_Player_Corner_Value) / (
                    Max_Player_Corner_Value + Min_Player_Corner_Value)
        else:
            Corner_Heuristic_Value = 0
        # print("Corner_Heuristic_Value:",Corner_Heuristic_Value)


        #stability

            
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]   
            
            
        Max_Player_Stability_Value=0
        Min_Player_Stability_Value=0

        if array[0][0] == 1:
            Max_Player_Stability_Value += 1    
        elif array[0][0] == -1:
            Min_Player_Stability_Value += 1
            
        if array[0][7] == 1:
            Max_Player_Stability_Value += 1
        elif array[0][7] == -1:
            Min_Player_Stability_Value += 1

        if array[7][0] == 1:
            Max_Player_Stability_Value += 1
        elif array[7][0] == -1:
            Min_Player_Stability_Value += 1

        if array[7][7] == 1:
            Max_Player_Stability_Value += 1
        elif array[7][7] == -1:
            Min_Player_Stability_Value += 1
            
            
        edge1_b = 0  
        flag1_b = 1  
        if array[0][0] == 1:
            for col in range(1, 8):
                if array[edge1_b][col] != 1:
                    flag1_b = 0
                    
            if(flag1_b == 1):        
                Max_Player_Stability_Value +=6
                
            
            
            
        edge1_w = 0  
        flag1_w = 1  
        if array[0][0] == -1:
            for col in range(1, 8):
                if array[edge1_w][col] != -1:
                    flag1_w = 0
                    
            if(flag1_w == 1):        
                Min_Player_Stability_Value +=6
                
                    
            
        edge2_b = 0  
        flag2_b = 1  
        if array[0][0] == 1:
            for row in range(1, 8):
                if array[row][edge2_b] != 1:
                    flag2_b = 0
            
            if(flag2_b == 1):        
                Max_Player_Stability_Value +=6
                


        edge2_w = 0  
        flag2_w = 1  
        if array[0][0] == -1:
            for row in range(1, 8):
                if array[row][edge2_w] != -1:
                    flag2_w = 0
            
            if(flag2_w == 1):        
                Min_Player_Stability_Value +=6
                
            

        edge3_b = 7  
        flag3_b = 1  
        if array[7][0] == 1:
            for col in range(1, 8):
                if array[edge3_b][col] != 1:
                    flag3_b = 0
                    
            if(flag3_b == 1):        
                Max_Player_Stability_Value +=6
                
                


        edge3_w = 7  
        flag3_w = 1  
        if array[7][0] == -1:
            for col in range(1, 8):
                if array[edge3_w][col] != -1:
                    flag3_w = 0
            
            if(flag3_w == 1):        
                Min_Player_Stability_Value +=6
                
            
            
                
            
        edge4_b = 7  
        flag4_b = 1  
        if array[0][7] == 1:
            for row in range(1, 8):
                if array[row][edge4_b] != 1:
                    flag4_b = 0
            
            if(flag4_b == 1):        
                Max_Player_Stability_Value +=6
                


        edge4_w = 7  
        flag4_w = 1  
        if array[0][7] == -1:
            for row in range(1, 8):
                if array[row][edge4_w] != -1:
                    flag4_w = 0
            
            if(flag4_w == 1):        
                Min_Player_Stability_Value +=6
                
            
        ##########################################################################################



        flag_try_b = 1
        if array[0][0] == 1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != 1:
                        flag_try_b = 0
                        
            if(flag_try_b == 1):
                Max_Player_Stability_Value +=1
                
                
                
        flag_try_w = 1
        if array[0][0] == -1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != -1:
                        flag_try_w = 0
                        
            if(flag_try_b == 1):
                Min_Player_Stability_Value +=1



        flag_try_b2 = 1
        if array[0][7] == 1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != 1:
                        flag_try_b2 = 0
                        
            if(flag_try_b == 1):
                Max_Player_Stability_Value +=1
                
                
                
        flag_try_w2 = 1
        if array[0][7] == -1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != -1:
                        flag_try_w2 = 0
                        
            if(flag_try_b == 1):
                Min_Player_Stability_Value +=1


        flag_try_b3 = 1
        if array[7][0] == 1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != 1:
                        flag_try_b3 = 0
                        
            if(flag_try_b == 1):
                Max_Player_Stability_Value +=1
                
                
                
        flag_try_w3 = 1
        if array[7][0] == -1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != -1:
                        flag_try_w3 = 0
                        
            if(flag_try_b == 1):
                Min_Player_Stability_Value +=1
                
        
                
        flag_try_b4 = 1
        if array[7][7] == 1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != 1:
                        flag_try_b4 = 0
                        
            if(flag_try_b == 1):
                Max_Player_Stability_Value +=1
                
                
                
        flag_try_w4 = 1
        if array[7][7] == -1:
            for x, y in directions:
                new_row = 0 + x
                new_col = 0 + y
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if array[new_row][new_col] != -1:
                        flag_try_w4 = 0
                        
            if(flag_try_b == 1):
                Min_Player_Stability_Value +=1
            
        
            
        
            
        
        # flag_try_b = 1
        # for row in range(8):
        #     for col in range(8):      
        #         if array[row][col] == 1:
        #             for x, y in directions:
        #                 new_row = row + x
        #                 new_col = col + y
                        
        #                 if 0 <= new_row < 8 and 0 <= new_col < 8:
        #                     if  array[new_row][new_col] != 1:
        #                         flag_try_b = 0
                                
        #                 if(flag_try_b == 1):
        #                     Max_Player_Stability_Value +=1
                            
                            
                                
                        
                            
                            
        # a = Helper()            
        
            
        # valid_Max = a.get_valid_moves(1, array)

        # for x, y in valid_Max:
        #     flip_Max = a.get_flipped_coins(x, y, 1, array)
            
        #     for z, k in flip_Max:
        #         Min_Player_Stability_Value -= 1
            


        # valid_Min = a.get_valid_moves(-1, array)
                
        # for x, y in valid_Min:
        #     flip_Min = a.get_flipped_coins(x, y, -1, array)
            
        #     for z, k in flip_Min:
        #         Max_Player_Stability_Value -= 1       
                    
                    
        if((Max_Player_Stability_Value+ Min_Player_Stability_Value) !=0):
            Stability_Heuristic_Value = 100* (Max_Player_Stability_Value - Min_Player_Stability_Value)/(Max_Player_Stability_Value+ Min_Player_Stability_Value)
        else:
            Stability_Heuristic_Value = 0
            
            
            
        #print("Max_Player_Stability_Value:")
        #print(Max_Player_Stability_Value)

        #print("Min_Player_Stability_Value:")
        #print(Min_Player_Stability_Value)

        #print("Stability_Heuristic_Value:")
        #print(Stability_Heuristic_Value)   


        # print(valid_Min)   
        # print(flip_Min) 



    

        # corner heuristic had a weight of 30
        # mobility heuristic had a weight of 5
        # stability heuristic had a weight of 25
        # coin parity heuristic also had a weight of 25.
        Total_heuristic_value = (0.3 * Corner_Heuristic_Value) + (0.05 * Mobility_value) + (0.25 * Stability_Heuristic_Value) + (
                0.25 * Coin_Parity_Heuristic_Value)
        # print("Total_heuristic_value:",Total_heuristic_value)
        return Total_heuristic_value



#Ai = Ai()

#print(Ai.get_best_move_Min([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]], 4))

#game = OthelloGame.Othello()
#game.first_screen()


