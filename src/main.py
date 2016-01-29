from sudoku import Sudoku

# Files must be in root directory
# param1: puzzle file, param2: solution file

if __name__ == "__main__":
    sudoku = Sudoku('easy240.txt', 'solution240.txt')
    sudoku.init_game()