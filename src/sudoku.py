# Thought process:
# Check whether position's row, col, and nonet already contain digit
# How should I structure my sudoku grid into code. Lists within lists? Multiple Arrays?
# With arrays in python, it is easy to determine if an item is in the list
# I need to be able to easily access the row, col, and each of 9 boxes
# Started out creating 2d arrays for rows, cols, nonets.
# Step one: Implement unique placement in row and column

# First Run with Row, Col, Nonet Rule in place: 42 wrong out of 81, not all zeros taken care of

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

    # Takes number and nonet number as param,
    # returns true if it is unique in it
    def valid_in_nonet(self, number, nonet_index):
        pass

    # Checks if game has been completed
    def is_complete(self):
        return self.all_boxes.count('0') == 0

    # Checks if solution is correct
    def check_solution(self):
        return self.rows == self.solution

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


    # Initialize game
    def init_game(self):
        for number in range(1, 10):
            for nonet in self.nonets:
                nonet_index = self.nonets.index(nonet)
                if str(number) not in nonet:
                    for box in nonet:
                        box_index = nonet.index(box)
                        if box == '0':
                            row_to_check = int(nonet_index / 3) * 3 + int(box_index / 3)
                            col_to_check = int(nonet_index % 3) * 3 + int(box_index % 3)
                            if self.valid_in_row(str(number), row_to_check) and self.valid_in_col(str(number), col_to_check):
                                    nonet[box_index] = str(number)
                                    self.cols[col_to_check][row_to_check] = str(number)
                                    self.rows[row_to_check][col_to_check] = str(number)
            if self.is_complete():
                self.game_complete = True
        print("My Answer: {}\n".format(self.rows))
        print("Solution: {}\n".format(self.solution))
        print("Number wrong: {}".format(self.get_number_wrong()))







s = Sudoku('../game.txt')

# s.all_boxes = [list(x) for x in s.all_boxes.split()] # rows
s.init_game()

