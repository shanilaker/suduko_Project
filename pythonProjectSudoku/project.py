import random

#An auxiliary function that returns the position on the Sudoku board
def position(n:int)->tuple:
    if 0 <= n <= 2:
        return 0,2

    elif 3 <= n <= 5:
        return 3, 5

    elif 6 <= n <= 8:
        return 6, 8

#An auxiliary function that returns the 3x3 board position of the point
def position_3x3(row,column)->list:
    return [position(row),position(column)]

"""
A function that receives a sudoku board and the position of a square
and returns the possible options for placement in this position
"""
def options(sudoku_board:list, loc:tuple)-> None or list:

    #If the cell contains a number it will return an empty list
    if sudoku_board[loc[0]][loc[1]] != -1:
        return []
    else:
        invalid_options_list = []
        #Checks which options are not possible because they are in a 3x3 square
        board_3x3 = position_3x3(loc[0],loc[1])
        for i in sudoku_board[board_3x3[0][0]:board_3x3[0][1]+1]:
            for j in i[board_3x3[1][0]:board_3x3[1][1] + 1]:
                if j != -1:
                    invalid_options_list.append(j)
        valid_options = []
        #Creates a list of options that are not in the 3x3 square
        for n in range(1,10):
            if n not in invalid_options_list:
                valid_options.append(n)

        #Deletes from the list all the members that are in the row of the member
        for x in sudoku_board[loc[0]]:
            if  (x != -1) and (x in valid_options):
                valid_options.remove(x)

        #Deletes from the list all the members that are in the column of the member
        for y in sudoku_board:
            if y[loc[1]] in valid_options:
                valid_options.remove((y[loc[1]]))

        #If there are no options, we will return an empty list
        if not valid_options:
            return None

        else:
            return valid_options

"""
A function that returns a sudoku board that in each slot 
there is a list of the options to be placed in each one
"""
def possible_digits(sudoku_board:list)->list:

    #Constructs an empty sudoku board
    options_board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1] for j in range(9)]

    #Fills the board by calling the function "options" on each cell in the board
    for y in range(len(options_board)):
        for x in range(len(options_board[y])):
            options_board[y][x] = options(sudoku_board, (int(y), int(x)))
    return options_board

#An auxiliary function for checking the correctness of the sudoku board
def valid_board(sudoku_board:list)->bool:

    #Checks that there are no repetitions in the rows
    for y in sudoku_board:
        for i in range(1,10):
            if y.count(i) > 1:
                return False

    #Checks that there are no repetitions in the columns
    for r in range(0,9):
        options_list = []
        for y in sudoku_board:
            options_list.append(y[r])
        for j in options_list:
            if (options_list.count(j) > 1) and (j != -1):
                return False

    #Checks that there are no repeats in 3x3 domains
    for z in range(0,9,3):
        for t in range(0,9,3):
            options_list3x3 = []
            for i in sudoku_board[z:z+3]:
                for j in i[t:t+3]:
                        options_list3x3.append(j)
            for j in options_list3x3:
                if (options_list3x3.count(j) > 1) and (j != -1):
                    return False

    #Checks that the values are 1-9
    for y in sudoku_board:
        for x in y:
            if (x > 9) or (x < 1):
                if x != -1:
                    return False
    return True

"""
A function that returns the position of the cell with the minimum number of options
"""
def min_slot(possibilities:list)->tuple:
    min_options_len_x = 0
    min_options_len_y = 0
    min_options_list = 9
    index_y = 0

    # Handles the values for the case if there is a slot that has not been filled
    for y in possibilities:
        index_x = 0
        for x in y:
            if len(x) > 1:
                if min_options_list > len(x):
                    min_options_len_x = index_x
                    min_options_len_y = index_y
                    min_options_list = len(x)
            index_x += 1
        index_y += 1

    return min_options_len_y, min_options_len_x


"""
A function that fills slots with one option to fill in a sudoku board
"""
def one_stage(sudoku_board:list, possibilities:list)->tuple:
    still_single_options = True

    while still_single_options:
        still_single_options = False
        index_y = 0
        more_than_one_option_x = 0

        for y in possibilities:
            index_x = 0

            #If the sudoku board is invalid, we will return FINISH_FAILURE
            if None in y or not valid_board(sudoku_board):
                return FINISH_FAILURE
            for x in y:

                #If there is one option to fill the slot, we will update the sudoku_board and the possibilities accordingly
                if len(x) == 1:
                    print((index_y,index_x))
                    sudoku_board[index_y][index_x] = x[0]
                    possibilities[index_y][index_x] = []

                    if not update_possibilities_per_slot_if_can(sudoku_board[index_y][index_x], (index_y,index_x), possibilities):
                        return FINISH_FAILURE

                    more_than_one_option_x += 1
                index_x += 1
            index_y += 1

        for p in possibilities:
            #Checks if there are more slots with a single option and will update the loop to continue accordingly
            for pos in p:
                if len(pos) == 1:
                    print(pos)
                    still_single_options = True
                    break
            if still_single_options:
                break

    # If there is a slot that has not been filled
    for y in sudoku_board:
        if -1 in y:
            return min_slot(possibilities), NOT_FINISH

    return FINISH_SUCCESS

"""
A function that updates the row,
the column and the 3x3 square of the same square
"""
def update_possibilities_per_slot_if_can(num:int, slot:tuple, possibilities:list)->bool:

    #Updating the column
    for y in possibilities:
        if num in y[slot[1]]:
            if len(y[slot[1]]) == 1:
                return False
            y[slot[1]].remove(num)

    #Updating the row
    for x in possibilities[slot[0]]:
        if num in x:
            if len(x) == 1:
                return False
            x.remove(num)

    #Updating the 3x3 area
    board_3x3 = position_3x3(slot[1],slot[0])
    for i in possibilities[board_3x3[1][0]:board_3x3[1][1] + 1]:
        for j in i[board_3x3[0][0]:board_3x3[0][1] + 1]:
            if num in j:
                if len(j) == 1:
                    return False
                j.remove(num)
    return True




"""
A function that fills the board with the help of the user
"""
def fill_board( sudoku_board:list, possibilities:list)->tuple:

    #Initial call to fill the board
    result = one_stage(sudoku_board,possibilities)
    print(possibilities)
    print(sudoku_board)
    #We will continue to fill the board until we have successfully filled it
    while result != (-2,-2):

        #If the first placement created duplicates
        if result == (-3, -3):
            return FINISH_FAILURE

        #As long as there are slots left to fill we will find them
        if result[1] == (-1, -1):
            square = result[0]

            #We will ask the user to choose the option to fill the slot, as long as it is in the options given to him
            user_input = int(input(f"Please enter the wanted option for square {square}, from this options list {possibilities[square[0]][square[1]]}: "))
            while user_input not in possibilities[square[0]][square[1]]:
                user_input = int(input(f"Please enter the wanted option for square {square}, from this options list {possibilities[square[0]][square[1]]}: "))

            #We will update the sudoku board and the possibilities list
            sudoku_board[square[0]][square[1]] = user_input
            possibilities[square[0]][square[1]] = []
            update_possibilities_per_slot_if_can(user_input, square, possibilities)

            print(possibilities)
            print(sudoku_board)
            #If the user's placement created an invalid board
            if not valid_board(sudoku_board):
                return FINISH_FAILURE
            result = one_stage(sudoku_board, possibilities)
            print(possibilities)

    return FINISH_SUCCESS

"""
A function that creates an initial board for the game
"""
def create_random_board(sudoku_board:list)->None:
    N = random.randrange(10,21)
    loc_list = []
    k_list =[i for i in range(1,81)]
    sudoku_board_copy = sudoku_board.copy()

    #Creates a list of the indexes of the slots in the board
    for i in range(0,9):
        for j in range(0,9):
            loc_list.append((i,j))
    while True:
        #fills the board N times
        for n in range(N):
            #Grill the position of the index in the loc_list that we would like to change according to the options for this cell
            loc_options = None
            while loc_options is None:
                K = random.choice(k_list)
                while loc_list[K] == -1:
                    K = random.choice(k_list)
                k_list.remove(K)
                # K = random.randrange(1, len(loc_list) + 1)
                print(K)
                loc_options = options(sudoku_board, loc_list[K])

            #Grill the number we want to fill in according to the options given to this slot
            loc_of_option = random.randrange(0,len(loc_options))
            index_value = loc_options[loc_of_option]

            #Update the board and delete this location from loc_list
            sudoku_board[loc_list[K][0]][loc_list[K][1]] = index_value
            loc_list[K] = -1

        if valid_board(sudoku_board_copy):
            sudoku_board.clear()
            sudoku_board += sudoku_board_copy
            return


"""
Receives a sudoku board and prints it in the desired format
"""

def print_board(sudoku_board:list)->None:
    #print("\n")
    print("-------------------")
    #Prints columns
    for i in range(9):
        print("|", end="")

        #Prints rows
        for j in range(9):
            if sudoku_board[i][j] == -1:
                print(" ",end="")
            else:
                print(sudoku_board[i][j], end = "")
            print("|", end="")
        print()
        print("-------------------")
        


"""
A function that prints the Sudoku board to a file
"""
def print_board_to_file(sudoku_board:list, f)->None:
    f.write("-------------------\n")
    #Prints columns
    for i in range(9):
        f.write("|")

        #Prints rows
        for j in range(9):
            if sudoku_board[i][j] == -1:
                f.write(" ")
            else:
                f.write(str(sudoku_board[i][j]))
            f.write("|")
        f.write("\n")
        f.write("-------------------\n")



def is_the_board_full(sudoku_board:list)->bool:
    for i in sudoku_board:
        if -1 in i:
            return False
    return True




example_board = [[5,3,-1,-1,7,-1,-1,-1,-1],
 [6,-1,-1,-1,-1,-1,1,-1,-1],
 [-1,-1,9,-1,-1,-1,-1,6,-1],
 [-1,-1,-1,-1,6,-1,-1,-1,3],
 [-1,-1,-1,8,-1,3,-1,-1,1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [-1,6,-1,-1,-1,-1,-1,-1,-1],
 [-1,-1,-1,-1,1,-1,-1,-1,-1],
 [-1,-1,-1,-1,8,-1,-1,-1,9]]

perfect_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

impossible_board = [[5,1,6,8,4,9,7,3,2],
 [3,-1,7,6,-1,5,-1,-1,-1],
 [8,-1,9,7,-1,-1,-1,6,5],
 [1,3,5,-1,6,-1,9,-1,7],
 [4,7,2,5,9,1,-1,-1,6],
 [9,6,8,3,7,-1,-1,5,-1],
 [2,5,3,1,8,6,-1,7,4],
 [6,8,4,2,-1,7,5,-1,-1],
 [7,9,1,-1,5,-1,6,-1,8]]

bug_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,9],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

# This board has two solutions - one for 2 and one for 4
interesting_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [-1,-1,-1,7,6,1,4,2,3],
 [-1,-1,-1,8,5,3,7,9,1],
 [-1,-1,-1,9,2,4,8,5,6],
 [-1,-1,-1,-1,3,7,2,8,4],
 [-1,-1,-1,-1,1,9,6,3,5],
 [-1,-1,-1,-1,8,6,1,7,9]]



NOT_FINISH = (-1,-1)
FINISH_SUCCESS = (-2,-2)
FINISH_FAILURE = (-3,-3)

rand_board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1] for j in range(9)]
create_random_board(rand_board)

list_of_boards = [perfect_board,rand_board, impossible_board, bug_board, interesting_board,example_board]
FILE_NAME = "solved_sudoku.txt"

with open(FILE_NAME, 'w') as f:
    for board in list_of_boards:
        if valid_board(board):
            if is_the_board_full(board):
                f.write("Here is the solved board\n")
                print_board_to_file(board, f)
            else:
                result = fill_board(board,possible_digits(board))
                if result == (-3,-3):
                    f.write("Board is unsolvable\n")
                elif result == (-2,-2):
                    print_board(board)
                    f.write("Here is the solved board\n")
                    print_board_to_file(board, f)
        else:
            print("Board is not legit!\n")
            f.write("Board is not legit!\n")



