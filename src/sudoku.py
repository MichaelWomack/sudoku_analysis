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
    # Tried row loop: 0,0
import time
class Sudoku:
    'Create an instance of Sudoku to solve'

    def __init__(self, file):
        self.game_string = open(file, 'r').read()
        self.all_boxes = open(file, 'r').read()
        self.solution = [list(x) for x in open('../solution.txt', 'r').read().split()]
        # self.rows = [list(row) for row in self.game_string.split()]
        # self.cols = [x[index] for x in self.rows for index in range(9)]
        self.rows = []
        self.cols = []
        self.nonets = []
        self.get_rows()
        self.get_cols()
        self.get_nonets()
        self.game_complete = False

    # Fills rows list from file data in appropriate format
    def get_rows(self):
        self.rows = [list(x) for x in self.all_boxes.split()]

    # Fills col list from file data
    def get_cols(self):
        for index in range(9):
            self.cols.append([x[index] for x in self.rows])

    # Fills list of nonets from game's file
    def get_nonets(self):
        index = 0
        row_start = 0
        row_end = 3
        for nonet_row in range(3):
            col_start = 0
            col_end = 3
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

    # Takes number and nonet number as param,
    # returns true if it is unique in it
    def num_empty_in_nonet(self, nonet_index):
        return self.nonets[nonet_index].count('0')

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
            row_index = self.rows.index(row)
            for box in row:
                box_index = row.index(box)
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
        invalid_indices = []
        box_index = 0
        for box in col:
            if box == '0' and box_index != validating_box_index:
                nonet_index = int(box_index / 3) * 3 + int(col_index / 3)
                if self.is_valid_placement(number, box_index, col_index, nonet_index):
                    only_valid_position = False
            box_index += 1
        return only_valid_position
        # for box in col:
        #     if box == '0' and box_index != validating_box_index:
        #         nonet_index = int(box_index / 3) * 3 + int(col_index / 3)
        #         if not self.is_valid_placement(number, validating_box_index, col_index, nonet_index):
        #             invalid_indices.append(box_index)
        #     box_index += 1
        #
        # box_index = 0
        # for box in col:
        #     if box == '0' and (box_index != validating_box_index or box_index in invalid_indices):
        #         nonet_index = int(box_index / 3) * 3 + int(col_index / 3)
        #         if self.is_valid_placement(number, validating_box_index, col_index, nonet_index):
        #             only_valid_position = False
        #     box_index += 1



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
                            self.cols[col_index][row_index] = str(number)
                            # self.nonets[nonet_index][box_index] = str(number) # this is the wrong box index
                            self.nonets[nonet_index][box_index] = str(number)
                            self.rows[row_index][col_index] = str(number)
                            print("----------Col ----- Added-------- ")
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
                            self.rows[row_index][col_index] = str(number)
                            self.cols[col_index][row_index] = str(number)
                            self.nonets[nonet_index][box_index] = str(number)
                            print("--------Row------Add_---------")
                            print("Row: {}, Col: {}, Nonet: {}, box_in_nonet: {}".format(row_index, col_index, nonet_index, box_index))
                    col_index += 1

    # Initialize game
    def init_game(self):

        while not self.game_complete:
            for number in range(1, 10):
                # Loops through nonets
                for nonet in self.nonets:
                    nonet_index = self.nonets.index(nonet)
                    if str(number) not in nonet:
                        box_index = 0
                        for box in nonet:
                            # print("Box: {}, Nonet: {}, Box: {}".format(box, nonet, nonet.index(box)))
                            if box == '0':
                                row_to_check = self.get_row_index_to_check(nonet_index, box_index)
                                col_to_check = self.get_col_index_to_check(nonet_index, box_index)
                                # print("Row: {}, Col: {}, Box: {}, Box Index: {} Nonet_Index: {}".format(row_to_check, col_to_check, box, box_index, nonet_index))
                                # time.sleep(5)
                                if self.is_valid_placement(str(number), row_to_check, col_to_check, nonet_index) and \
                                        self.only_valid_position_in_nonet(nonet_index, box_index, str(number)):

                                        # self.only_valid_number(nonet_index, row_to_check, col_to_check, str(number)):

                                        self.nonets[nonet_index][box_index] = str(number)
                                        self.cols[col_to_check][row_to_check] = str(number)
                                        self.rows[row_to_check][col_to_check] = str(number)

                                        print("Mine: {}".format(self.rows))
                                        print("Actual: {}".format(self.solution))
                                        print("Row:{} Index:{} Number Placed: {}".format(row_to_check, col_to_check, str(number)))
                                        time.sleep(.5)
                            box_index += 1
                #self.check_cols(str(number))
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
                                            self.cols[col_index][row_index] = str(number)
                                            # self.nonets[nonet_index][box_index] = str(number) # this is the wrong box index
                                            self.nonets[nonet_index][box_index] = str(number)
                                            self.rows[row_index][col_index] = str(number)
                                            print("----------Col ----- Added-------- ")
                            row_index += 1

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
                                        self.rows[row_index][col_index] = str(number)
                                        self.cols[col_index][row_index] = str(number)
                                        self.nonets[nonet_index][box_index] = str(number)
                                        print("--------Row------Add_---------")
                                        print("Row: {}, Col: {}, Nonet: {}, box_in_nonet: {}".format(row_index, col_index, nonet_index, box_index))
                            col_index += 1



            # print("My Answer: {}\n".format(self.rows))
            print("My Answer: ")
            self.print_rows()
            print("Solution: {}\n".format(self.solution))
            print("Number wrong: {}".format(self.get_number_wrong()))
            print("Number empty: {}".format(self.get_number_empty()))
            time.sleep(1)
            if self.is_complete() or (time.process_time() > 5):
                self.game_complete = True
        print("My Answer: {}\n".format(self.rows))
        print("Solution: {}\n".format(self.solution))
        print("Number wrong: {}".format(self.get_number_wrong()))
        print("Number empty: {}".format(self.get_number_empty()))


s = Sudoku('../game.txt')

# s.all_boxes = [list(x) for x in s.all_boxes.split()] # rows

s.init_game()


