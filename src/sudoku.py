# Thought process:
# Check whether position's row, col, and nonet already contain digit
# How should I structure my sudoku grid into code. Lists within lists? Multiple Arrays?
# With arrays in python, it is easy to determine if an item is in the list
# I need to be able to easily access the row, col, and each of 9 boxes
# Started out creating 2d arrays for rows, cols, nonets.
# Step one: Implement unique placement in row and column

# First Run with Row, Col, Nonet Rule in place: 42 wrong out of 81, not all zeros taken care of
# Adding loop that runs through Rows and does check: 39 wrong out of 81, 22 empty
# Adding loop that runs through cols and does check: 38 wrong out of 81, 21 empty
# Best with large loop, no lockup: 36 wrong, 16 empty
# I started solving sudoku in real life. Realized I need to start with nonet or col or row with least blanks

# Started with checking if the number is in the nonet.
# Note. With row, col, nonet, and is_valid_placement: 36 wrong, 11 empty
# Note. With row, col, nonet, is_valid_placement and only_valid_placement: 52 wrong, 52 empty

#Puzzle 237 : with col,row, nonet, only_valid_placement: 26 wrong, 26 empty. Definitely check
    # Stops, doesn't know that a column only has one position left,

    # Added column loop in init(): 24 wrong, 24 empty?????
    # Column loop bug: 20 wrong, 19 empty
    # Fixed column bug: 22 wrong, 22 empty
    # Tried row loop: 0,0 ********************************************************
#
import time
class Sudoku:
    'Create an instance of Sudoku to solve'

    def __init__(self, file, solution):
        self.all_boxes = open('../' + file, 'r').read()
        self.solution = [list(x) for x in open('../' + solution, 'r').read().split()]
        self.rows = [list(row) for row in self.all_boxes.split()]
        self.cols, self.nonets = [], []
        self.game_complete = False

    # Fills col list from file data
    def get_cols(self):
        for index in range(9):
            self.cols.append([x[index] for x in self.rows])

    # Fills list of nonets from game's file
    def get_nonets(self):
        index, row_start, row_end = 0, 0, 3
        for nonet_row in range(3):
            col_start, col_end = 0, 3
            for nonet_col in range(3):
                self.nonets.append([])
                for row in self.rows[row_start:row_end]:
                    self.nonets[index].extend([x for x in row[col_start:col_end]])
                index += 1
                col_start += 3
                col_end += 3
            row_start += 3
            row_end += 3

    # Takes number and row index as param,
    # returns true if it is unique in its row
    def valid_in_row(self, number, row_index):
        return self.rows[row_index].count(number) == 0

    # Takes number and column index as param,
    # returns true if it is unique in its column
    def valid_in_col(self, number, col_index):
        return self.cols[col_index].count(number) == 0

    def valid_in_nonet(self, number, nonet_index):
        return self.nonets[nonet_index].count(number) == 0

    def is_valid_placement(self, number, row_index, col_index, nonet_index):
        return self.valid_in_row(number, row_index) and \
            self.valid_in_col(number, col_index) and \
            self.valid_in_nonet(number, nonet_index)

    # Checks if game has been completed
    def is_complete(self):
        done = True
        for row in self.rows:
            if '0' in row:
                done = False
        return done

    # Checks if solution is correct
    def check_solution(self):
        return self.rows == self.solution

    def print_rows(self):
        for row in self.rows:
            print("".join([x for x in row]))

    def print_solution(self):
        for row in self.solution:
            print("".join([x for x in row]))

    # Counts number of wrong boxes by comparing with solution
    def get_number_wrong(self):
        num_wrong = 0
        for row in self.rows:
            row_index = self.rows.index(row)
            for box in row:
                box_index = row.index(box)
                if box != self.solution[row_index][box_index]:
                    num_wrong += 1
        return num_wrong

    def get_number_empty(self):
        num_empty = 0
        for row in self.rows:
            for box in row:
                if box == '0':
                    num_empty += 1
        return num_empty

    def get_row_index_to_check(self, nonet_index, box_index):
        return int(nonet_index / 3) * 3 + int(box_index / 3)

    def get_col_index_to_check(self, nonet_index, box_index):
        return int(nonet_index % 3) * 3 + int(box_index % 3)

    def only_valid_position_in_nonet(self, nonet_index, validating_box_index, number):
        nonet = self.nonets[nonet_index]
        only_valid_position = True
        box_index = 0
        for box in nonet:
            if box == '0' and box_index != validating_box_index:
                check_row = self.get_row_index_to_check(nonet_index, box_index)
                check_col = self.get_col_index_to_check(nonet_index, box_index)
                if self.is_valid_placement(number, check_row, check_col, nonet_index):
                    only_valid_position = False
            box_index += 1
        return only_valid_position

    # Checks that the box in the column
    def only_valid_position_in_col(self, col_index, validating_box_index, number):
        col = self.cols[col_index]
        only_valid_position = True
        box_index = 0
        for box in col:
            if box == '0' and box_index != validating_box_index:
                nonet_index = int(box_index / 3) * 3 + int(col_index / 3)
                if self.is_valid_placement(number, box_index, col_index, nonet_index):
                    only_valid_position = False
            box_index += 1
        return only_valid_position

    def only_valid_position_in_row(self, row_index, validating_box_index, number):
        row = self.rows[row_index]
        only_valid_position = True
        box_index = 0
        for box in row:
            if box == '0' and box_index != validating_box_index:
                nonet_index = int(row_index / 3) * 3 + int(box_index / 3)
                if self.is_valid_placement(number, row_index, box_index, nonet_index):
                    only_valid_position = False
            box_index += 1
        return only_valid_position

    def only_valid_number(self, nonet_index, row_index, col_index, number):
        only_valid_number = True
        for num in range(1, 10):
            if str(num) != number:
                if self.valid_in_row(number, row_index) and \
                        self.valid_in_col(number, col_index) and \
                        self.valid_in_nonet(number, nonet_index):
                    only_valid_number = False
        return only_valid_number

    def check_nonets(self, number):
        for nonet in self.nonets:
            nonet_index = self.nonets.index(nonet)
            if str(number) not in nonet:
                box_index = 0
                for box in nonet:
                    if box == '0':
                        row_to_check = self.get_row_index_to_check(nonet_index, box_index)
                        col_to_check = self.get_col_index_to_check(nonet_index, box_index)
                        if self.is_valid_placement(str(number), row_to_check, col_to_check, nonet_index) and\
                                self.only_valid_position_in_nonet(nonet_index, box_index, str(number)):
                            self.set_value(row_to_check, col_to_check, nonet_index, box_index, str(number))
                    box_index += 1

    def check_cols(self, number):
        for col in self.cols:
            col_index = self.cols.index(col)
            if str(number) not in col:
                row_index = 0
                for box in col:
                    if box == '0':
                        nonet_index = int(row_index / 3) * 3 + int(col_index / 3)
                        box_index = (row_index % 3) * 3 + (col_index % 3)
                        if self.is_valid_placement(str(number), row_index, col_index, nonet_index) and \
                                self.only_valid_position_in_col(col_index, row_index, str(number)):
                            self.set_value(row_index, col_index, nonet_index, box_index, str(number))
                    row_index += 1

    def check_rows(self, number):
        for row in self.rows:
            row_index = self.rows.index(row)
            if str(number) not in row:
                col_index = 0
                for box in row:
                    if box == '0':
                        box_index = (row_index % 3) * 3 + (col_index % 3)
                        nonet_index = int(row_index / 3) * 3 + int(col_index / 3)
                        if self.is_valid_placement(str(number), row_index, col_index, nonet_index) and \
                                self.only_valid_position_in_row(row_index, col_index, str(number)):
                            self.set_value(row_index, col_index, nonet_index, box_index, str(number))
                    col_index += 1

    def set_value(self, row_index, col_index, nonet_index, box_index, number):
        self.rows[row_index][col_index] = number
        self.cols[col_index][row_index] = number
        self.nonets[nonet_index][box_index] = number

    # Initialize game
    def init_game(self):
        # fill game structures
        self.get_cols()
        self.get_nonets()

        while not self.game_complete:
            for number in range(1, 10):
                self.check_nonets(number)
                self.check_cols(number)
                self.check_rows(number)
            # time.sleep(.1)
            print("\nMy Answer: ")
            self.print_rows()
            print("\nNumber wrong: {}\nNumber empty: {}\n".format(
                    self.get_number_wrong(), self.get_number_empty()))
            # time.sleep(.5)

            if self.is_complete() or (time.process_time() > 2):
                self.game_complete = True

        print("----------------Analysis Results-----------------")
        print("\nMy Answer: ")
        self.print_rows()
        print("\nSolution: ")
        self.print_solution()
        print("\nNumber wrong: {}\nNumber empty: {}\n".format(
                self.get_number_wrong(), self.get_number_empty()))

s = Sudoku('easy240.txt', 'solution240.txt')
s.init_game()
