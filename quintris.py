#Simple quintris program! v0.2
# D. Crandall, Sept 2021
from click._compat import raw_input

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import copy
import queue




class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = raw_input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()



class ComputerPlayer:


    def get_config_string(self,state_config):
        col1 = state_config[1]
        rotation = state_config[2]
        final_config = []
        k = 0


        while k == 0:
            if rotation == 0:
                k = 1
            elif rotation == 1:
                final_config.append("n")
                k = 1
            elif rotation == 2:
                final_config.append("nn")
                k = 1
            elif rotation == 3:
                final_config.append("nnn")
                k = 1


        quintris_col = quintris.col

        g = 0
        while g == 0:
            if (col1 < quintris_col):
                final_config.append("b")
                quintris_col -= 1
            elif (col1 > quintris_col):
                final_config.append("m")
                quintris_col += 1
            else:
                g = 1


        final_config_string = ''.join(final_config)


        return final_config_string




    def calculate_heuristic(self,h_quintris):
        heuristic1 = 0
        state_board = h_quintris.get_board()



        column_heights = [
            min([r for r in range(len(state_board[0]) - 1, 0, -1) if state_board[r][c] == "x"] + [100, ]) for c
            in range(0, len(state_board[0]))]
        column_heights_updated = []
        for i in column_heights:
            if i == 100:
                each_col_height = 0
            else:
                each_col_height = 20 - i
            column_heights_updated.append(each_col_height)

        aggre_col_height = sum(column_heights_updated)


        holes = 0
        holes = 0
        for row in range(19, 0, -1):
            for col in range(0, 10):
                if state_board[row][col] == " " and state_board[row - 1][col] == 'x':
                    holes += 1


        trench_list = []
        for i in range(0, len(column_heights_updated) - 1):
            s = abs(column_heights_updated[i] - column_heights_updated[i + 1])
            trench_list.append(s)
        trench = sum(trench_list)


        row_cleared = 0
        for row in range(19, 0, -1):
            filled = 0
            for col in range(0, 10):
                if state_board[row][col] == 'x':
                    filled += 1
            if filled == 10:
                row_cleared += 1


        state_piece = copy.deepcopy(h_quintris.get_piece())
        for col in range(0, 10):
            for row in range(len(state_piece[0]), 20):
                if state_board[row][col] == ' ':
                    if col != 0:
                        if state_board[row][col - 1] == 'x':
                            heuristic1 += (20 - row)
                        elif state_board[row][col] == 'x':
                            heuristic1 += (20 - row)
                if state_board[row][col] == ' ':
                    if state_board[row - 1][col] == 'x':
                        heuristic1 += (20 - row) ** 2
                if state_board[row][col] == ' ':
                    if col != 9:
                        if state_board[row][col + 1] == 'x':
                            heuristic1 += (20 - row)
                        elif state_board[row][col] == 'x':
                            heuristic1 += (20 - row)





        # calculate heuristic
        # a *(Aggregate Height) + b * (Complete Lines) + c *(Holes) + d *(trench)
        # Reference : - https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        heuristic2 = (-0.5100666 * aggre_col_height) + (0.760666 * row_cleared) + (-0.35663 * holes) + (-0.184483 * trench)
        heuristic3 = heuristic1 * 2 + heuristic2

        return (heuristic1,heuristic3)


    def get_moves(self, quintris):

        next_piece_heuristic = 0
        temp_heu_state = []
        current_piece_heuristic = 0
        heuristic_for_states = []
        newtetris = copy.deepcopy(quintris)
        board = copy.deepcopy(newtetris.get_board())
        current_piece = copy.deepcopy(newtetris.get_piece())
        next_piece = copy.deepcopy(newtetris.get_next_piece())
        current_piece_rotations = []
        next_piece_rotations = []
        possible_state_with_heuristic = queue.Queue.PriorityQueue()

        rotation_angles = [90, 180, 270]

        current_piece_rotations.append(copy.deepcopy(current_piece)[0])
        for i in rotation_angles:
            current_piece_rotations.append(QuintrisGame.rotate_piece(current_piece[0], i))


        next_piece_rotations.append(copy.deepcopy(next_piece))
        for i in rotation_angles:
            next_piece_rotations.append(QuintrisGame.rotate_piece(next_piece, i))



        #Iterating through all the current piece possible rotations
        for piece in current_piece_rotations:
            #Iterating through the board and placing piece on each possible position
            for col_main in range(0,11 - len(piece[0])):
                current_piece_heuristic = 0

                temptetris = copy.deepcopy(quintris)
                temptetris_piece = copy.deepcopy(temptetris.get_piece())

                temptetris_piece_col = temptetris_piece[2]
                temptetris.piece = copy.deepcopy(piece)
                n = 0

                while (n == 0):
                    if (col_main < temptetris_piece_col):
                        temptetris.left()
                        temptetris_piece_col -= 1
                    elif (col_main > temptetris_piece_col):
                        temptetris.right()
                        temptetris_piece_col += 1
                    else:

                        temptetris.down("heu")
                        current_state_board = copy.deepcopy(temptetris.get_board())

                        current_piece_heuristic = self.calculate_heuristic(copy.deepcopy(temptetris))

                        n = 1


                for next_piece in next_piece_rotations:
                    for col in range(0, 10 - len(next_piece[0])):
                        next_piece_heuristic = 0
                        temp_heu_state[:] = []
                        temptetris1 = copy.deepcopy(temptetris)
                        temptetris_piece1 = copy.deepcopy(temptetris1.get_piece())
                        temptetris_piece_col1 = temptetris_piece1[2]
                        temptetris.piece = copy.deepcopy(next_piece)
                        d = 0
                        while (d == 0):
                            if (col < temptetris_piece_col1):
                                temptetris1.left()
                                temptetris_piece_col1 -= 1
                            elif (col > temptetris_piece_col1):
                                temptetris1.right()
                                temptetris_piece_col1 += 1
                            else:
                                temptetris1.down("heu")
                                next_state_board = copy.deepcopy(temptetris1.get_board())

                                next_piece_heuristic = self.calculate_heuristic(copy.deepcopy(temptetris1))
                                temp_heu_state.append(current_piece_heuristic + next_piece_heuristic)
                                temp_heu_state.append(col_main)
                                temp_heu_state.append(current_piece_rotations.index(piece))
                                # print "heu for next state",temp_heu_state
                                heuristic_for_states.append(temp_heu_state)
                                # print "heuristic_for_states", heuristic_for_states
                                possible_state_with_heuristic.put((current_piece_heuristic + next_piece_heuristic,col_main,current_piece_rotations.index(piece)))
                                d = 1

                possible_state_with_heuristic.put((current_piece_heuristic[0],col_main,current_piece_rotations.index(piece)))


        best_placement = possible_state_with_heuristic.get()


        final_config_string = copy.deepcopy(self.get_config_string(best_placement))

        return final_config_string




    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [min([r for r in range(len(board) - 1, 0, -1) if board[r][c] == "x"] + [100, ]) for c in
                              range(0, len(board[0]))]
            index = column_heights.index(max(column_heights))

            if (index < quintris.col):
                quintris.left()
            elif (index > quintris.col):
                quintris.right()
            else:
                quintris.down("heu")


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]
try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



