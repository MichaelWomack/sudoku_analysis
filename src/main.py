from sudoku import Sudoku

# Files must be in puzzles directory
# param1: puzzle fileName, param2: solution fileName

if __name__ == "__main__":
    sudoku = Sudoku('easy235.txt', 'solution235.txt')
    sudoku.init_game()