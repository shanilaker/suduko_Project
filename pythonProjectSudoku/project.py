import random


#A helper function that returns the position in the range 0-8 of an index
def position(n: int) -> tuple:
    if 0 <= n <= 2:
        return 0, 2

    elif 3 <= n <= 5:
        return 3, 5

    elif 6 <= n <= 8:
        return 6, 8

# A helper function that returns the 3x3 board position of the point
def position_3x3(row, column) -> list:
    return [position(row), position(column)]

"""
A function that receives a sudoku board and the position of a square
and returns the possible options for placement in this position
"""
def options(sudoku_board: list, loc: tuple) -> None or list:

    # If the cell contains a number it will return an empty list
    if sudoku_board[loc[0]][loc[1]] != -1:
        return []
    else:
        invalid_options_list = []

        # Checks which options are not possible because they are in a 3x3 square
        board_3x3 = position_3x3(loc[0], loc[1])
        for rows in sudoku_board[board_3x3[0][0]:board_3x3[0][1] + 1]:
            for n1 in rows[board_3x3[1][0]:board_3x3[1][1] + 1]:
                if n1 != -1:
                    invalid_options_list.append(n1)
        valid_options = []

        # Creates a list of options that are not in the 3x3 square
        for n2 in range(1, 10):
            if n2 not in invalid_options_list:
                valid_options.append(n2)

        # Deletes from the list all the members that are in the row of the member
        for n3 in sudoku_board[loc[0]]:
            if (n3 != -1) and (n3 in valid_options):
                valid_options.remove(n3)

        # Deletes from the list all the members that are in the column of the member
        for row in sudoku_board:
            if row[loc[1]] in valid_options:
                valid_options.remove((row[loc[1]]))

        # If there are no options, we will return None
        if not valid_options:
            return None

        else:
            return valid_options

"""
A function that returns a sudoku board that in each slot 
there is a list of the options to be placed in each one
"""
def possible_digits(sudoku_board: list) -> list:
    # Constructs an empty sudoku board
    options_board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1] for j in range(9)]

    # Fills the board by calling the function "options" on each cell in the board
    for row in range(len(options_board)):
        for column in range(len(options_board[row])):
            options_board[row][column] = options(sudoku_board, (row, column))
    return options_board

#A helper function that checks that there are no repeats in 3x3 domains
def repetitions_3x3(sudoku_board:list):
    for n1 in range(0, 9, 3):
        for n2 in range(0, 9, 3):
            options_list3x3 = []
            for rows in sudoku_board[n1:n1 + 3]:
                for columns in rows[n2:n2 + 3]:
                    options_list3x3.append(columns)

            for option in options_list3x3:
                if (options_list3x3.count(option) > 1) and (option != -1):
                    return False
    return True

#A helper function for checking the correctness of the sudoku board
def valid_board(sudoku_board: list) -> bool:
    # Checks that there are no repetitions in the rows
    for row1 in sudoku_board:
        for n in range(1, 10):
            if row1.count(n) > 1:
                return False

    # Checks that there are no repetitions in the columns
    for column in range(0, 9):
        options_list = []
        for row2 in sudoku_board:
            options_list.append(row2[column])

        for op in options_list:
            if (options_list.count(op) > 1) and (op != -1):
                return False

    #Checks that there are no repeats in 3x3 domains
    if not repetitions_3x3(sudoku_board):
        return False

    # Checks that the values are 1-9
    for row3 in sudoku_board:
        for n3 in row3:
            if (n3 > 9) or (n3 < 1):
                if n3 != -1:
                    return False

    return True

"""
A function that returns the position of the cell with the minimum number of options
"""
def min_slot(possibilities: list) -> tuple:
    min_options_len_column = 0
    min_options_len_row = 0
    min_options_list_len = 9
    index_row = 0

    # Searches for the cell with the minimum number of options
    for row in possibilities:
        index_column = 0

        for column in row:
            if len(column) > 1:
                if min_options_list_len > len(column):
                    min_options_len_column = index_column
                    min_options_len_row = index_row
                    min_options_list_len = len(column)
            index_column += 1
        index_row += 1

    return min_options_len_row, min_options_len_column

"""
A function that fills slots with one option to fill in a sudoku board
"""
def one_stage(sudoku_board: list, possibilities: list) -> tuple:
    still_single_options = True

    while still_single_options:
        still_single_options = False
        index_row = 0

        for row in possibilities:
            index_column = 0

            # If the sudoku board is invalid, we will return FINISH_FAILURE
            if None in row or not valid_board(sudoku_board):
                return FINISH_FAILURE

            for options_list in row:

                # If there is one option to fill the slot, we will update the sudoku_board and the possibilities accordingly
                if len(options_list) == 1:
                    sudoku_board[index_row][index_column] = options_list[0]
                    possibilities[index_row][index_column] = []

                    if not update_possibilities_per_slot_if_can(sudoku_board[index_row][index_column], (index_row, index_column),possibilities):
                        return FINISH_FAILURE
                index_column += 1
            index_row += 1

        #checks if there are more slots with a single option and will update the loop to continue accordingly
        still_single_options = still_single_option(possibilities)

    # If there is a slot that has not been filled
    for y in sudoku_board:
        if -1 in y:
            return min_slot(possibilities), NOT_FINISH

    return FINISH_SUCCESS

#Helper function that checks if there are more slots with a single option
def still_single_option(possibilities:list)->bool:
    for p in possibilities:
        for pos in p:
            if len(pos) == 1:
                return True
    return False

"""
A function that updates the row,
the column and the 3x3 square of the same square
"""
def update_possibilities_per_slot_if_can(num: int, slot: tuple, possibilities: list) -> bool:
    # Updating the column
    for column in possibilities:
        if num in column[slot[1]]:
            if len(column[slot[1]]) == 1:
                return False
            column[slot[1]].remove(num)

    # Updating the row
    for row in possibilities[slot[0]]:
        if num in row:
            if len(row) == 1:
                return False
            row.remove(num)

    # Updating the 3x3 area
    board_3x3 = position_3x3(slot[1], slot[0])
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
def fill_board(sudoku_board: list, possibilities: list) -> tuple:
    # Initial call to fill the board
    result = one_stage(sudoku_board, possibilities)

    # We will continue to fill the board until we have successfully filled it
    while result != (-2, -2):

        # If the first placement created duplicates
        if result == (-3, -3):
            return FINISH_FAILURE

        # As long as there are slots left to fill we will find them
        if result[1] == (-1, -1):
            square = result[0]

            # We will ask the user to choose the option to fill the slot, as long as it is in the options given to him
            user_input = int(input(
                f"Please enter the wanted option for square {square}, from this options list {possibilities[square[0]][square[1]]}: "))
            while user_input not in possibilities[square[0]][square[1]]:
                user_input = int(input(
                    f"Please enter the wanted option for square {square}, from this options list {possibilities[square[0]][square[1]]}: "))

            # We will update the sudoku board and the possibilities list
            sudoku_board[square[0]][square[1]] = user_input
            possibilities[square[0]][square[1]] = []
            update_possibilities_per_slot_if_can(user_input, square, possibilities)

            # If the user's placement created an invalid board
            if not valid_board(sudoku_board):
                return FINISH_FAILURE
            result = one_stage(sudoku_board, possibilities)

    return FINISH_SUCCESS

"""
A function that creates a board for the game
"""
def create_random_board(sudoku_board: list) -> None:
    N = random.randrange(10, 21)
    loc_list = []
    k_list = [i for i in range(1, 81)]
    sudoku_board_copy = sudoku_board.copy()

    # Creates a list of the indexes of the slots in the board
    for row in range(0, 9):
        for column in range(0, 9):
            loc_list.append((row, column))

    while True:

        # fills the board N times
        for n in range(N):

            # Grill the position of the index in the loc_list that we would like to change according to the options for this cell
            loc_options = None
            while loc_options is None:
                K = random.choice(k_list)

                while loc_list[K] == -1:
                    K = random.choice(k_list)
                k_list.remove(K)
                loc_options = options(sudoku_board, loc_list[K])

            # Grill the number we want to fill in according to the options given to this slot
            loc_of_option = random.randrange(0, len(loc_options))
            index_value = loc_options[loc_of_option]

            # Update the board and updates accordingly this location in loc_list
            sudoku_board[loc_list[K][0]][loc_list[K][1]] = index_value
            loc_list[K] = -1

        #Updates the board
        if valid_board(sudoku_board_copy):
            sudoku_board.clear()
            sudoku_board += sudoku_board_copy
            return

"""
Receives a sudoku board and prints it in the desired format
"""
def print_board(sudoku_board: list) -> None:
    print("-------------------")

    # Prints columns
    for row in range(9):
        print("|", end="")

        # Prints rows
        for column in range(9):
            if sudoku_board[row][column] == -1:
                print(" ", end="")
            else:
                print(sudoku_board[row][column], end="")
            print("|", end="")
        print()
        print("-------------------")

"""
A function that prints the Sudoku board to a file
"""
def print_board_to_file(sudoku_board: list, f) -> None:
    f.write("-------------------\n")

    # Prints columns
    for row in range(9):
        f.write("|")

        # Prints rows
        for column in range(9):
            if sudoku_board[row][column] == -1:
                f.write(" ")
            else:
                f.write(str(sudoku_board[row][column]))
            f.write("|")
        f.write("\n")
        f.write("-------------------\n")

#A helper function that checks whether the board is full
def is_the_board_full(sudoku_board: list) -> bool:
    for row in sudoku_board:
        if -1 in row:
            return False
    return True


example_board = [[5, 3, -1, -1, 7, -1, -1, -1, -1],
                 [6, -1, -1, -1, -1, -1, 1, -1, -1],
                 [-1, -1, 9, -1, -1, -1, -1, 6, -1],
                 [-1, -1, -1, -1, 6, -1, -1, -1, 3],
                 [-1, -1, -1, 8, -1, 3, -1, -1, 1],
                 [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                 [-1, 6, -1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, 1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, 8, -1, -1, -1, 9]]

perfect_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                 [6, 7, 2, 1, 9, 5, 3, 4, 8],
                 [1, 9, 8, 3, 4, 2, 5, 6, 7],
                 [8, 5, 9, 7, 6, 1, 4, 2, 3],
                 [4, 2, 6, 8, 5, 3, 7, 9, 1],
                 [7, 1, 3, 9, 2, 4, 8, 5, 6],
                 [9, 6, 1, 5, 3, 7, 2, 8, 4],
                 [2, 8, 7, 4, 1, 9, 6, 3, 5],
                 [3, 4, 5, 2, 8, 6, 1, 7, 9]]

impossible_board = [[5, 1, 6, 8, 4, 9, 7, 3, 2],
                    [3, -1, 7, 6, -1, 5, -1, -1, -1],
                    [8, -1, 9, 7, -1, -1, -1, 6, 5],
                    [1, 3, 5, -1, 6, -1, 9, -1, 7],
                    [4, 7, 2, 5, 9, 1, -1, -1, 6],
                    [9, 6, 8, 3, 7, -1, -1, 5, -1],
                    [2, 5, 3, 1, 8, 6, -1, 7, 4],
                    [6, 8, 4, 2, -1, 7, 5, -1, -1],
                    [7, 9, 1, -1, 5, -1, 6, -1, 8]]

bug_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
             [6, 7, 2, 1, 9, 5, 3, 4, 9],
             [1, 9, 8, 3, 4, 2, 5, 6, 7],
             [8, 5, 9, 7, 6, 1, 4, 2, 3],
             [4, 2, 6, 8, 5, 3, 7, 9, 1],
             [7, 1, 3, 9, 2, 4, 8, 5, 6],
             [9, 6, 1, 5, 3, 7, 2, 8, 4],
             [2, 8, 7, 4, 1, 9, 6, 3, 5],
             [3, 4, 5, 2, 8, 6, 1, 7, 9]]

# This board has two solutions - one for 2 and one for 4
interesting_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                     [6, 7, 2, 1, 9, 5, 3, 4, 8],
                     [1, 9, 8, 3, 4, 2, 5, 6, 7],
                     [-1, -1, -1, 7, 6, 1, 4, 2, 3],
                     [-1, -1, -1, 8, 5, 3, 7, 9, 1],
                     [-1, -1, -1, 9, 2, 4, 8, 5, 6],
                     [-1, -1, -1, -1, 3, 7, 2, 8, 4],
                     [-1, -1, -1, -1, 1, 9, 6, 3, 5],
                     [-1, -1, -1, -1, 8, 6, 1, 7, 9]]

NOT_FINISH = (-1, -1)
FINISH_SUCCESS = (-2, -2)
FINISH_FAILURE = (-3, -3)

#Create a new sudoku board
rand_board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1] for j in range(9)]
create_random_board(rand_board)

list_of_boards = [perfect_board, rand_board, impossible_board, bug_board, interesting_board, example_board]
FILE_NAME = "solved_sudoku.txt"

#Enters the sudoku solving results in a file
with open(FILE_NAME, 'w') as f:
    for board in list_of_boards:
        if valid_board(board):
            if is_the_board_full(board):
                f.write("Here is the solved board\n")
                print_board_to_file(board, f)

            else:
                result = fill_board(board, possible_digits(board))
                if result == (-3, -3):
                    f.write("Board is unsolvable\n")

                elif result == (-2, -2):
                    f.write("Here is the solved board\n")
                    print_board_to_file(board, f)

        else:
            f.write("Board is not legit!\n")