# Thought process:
# Check whether position's row, col, and nonet already contain digit
# How should I structure my sudoku grid into code. Lists within lists? Multiple Arrays?
# With arrays in python, it is easy to determine if an item is in the list
# I need to be able to easily access the row, col, and each of 9 boxes
# Started out creating 2d arrays for rows, cols, nonets.
# Step one: Implement unique placement in row and column


class Sudoku:
    'Create an instance of Sudoku to solve'

    def __init__(self, file):
        self.all_boxes = open(file, 'r').read()
        self.solution = open('../solution.txt', 'r').read()
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

    # Stores nonets as lists
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
        return self.all_boxes == open('../solution.txt', 'r').read()

    # Counts number of wrong boxes by comparing with solution
    def get_number_wrong(self):
        solution = list(open('../solution.txt', 'r').read())
        num_wrong = 0
        for box in list(self.all_boxes):
            if box != solution[self.all_boxes.index(box)]:
                num_wrong += 1
        return num_wrong


    # Initialize game
    # def init_game(self):
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #     print("\nMy answer: \n{}".format(self.all_boxes))
    #     print("\nCorrect Solution: \n{}".format(self.solution))
    #     print("\nNumber of Wrong Placements: {}".format(self.get_number_wrong()))

s = Sudoku('../game.txt')
print(s.nonets)
#print(s.all_boxes.split('\n'))
# print(s.all_boxes)
# print(s.valid_in_row('3', 0))
# print("is complete: {}".format(s.is_complete()))
# s.init_game()