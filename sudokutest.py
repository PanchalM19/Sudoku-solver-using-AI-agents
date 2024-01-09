import sudokuboards
import sudokuagents
import numpy as np
from time import perf_counter

board = sudokuboards.easy
# board = sudokuboards.medium
# board = sudokuboards.difficult
# board = sudokuboards.vDifficult
# board = sudokuboards.hardestSudoku
# board = sudokuboards.AI_Escargot
# board = sudokuboards.steeringWheel
# board = sudokuboards.blondePlatine
# board = sudokuboards.artoInkala

# agent = sudokuagents.backtracking()
# agent = sudokuagents.knuth()
agent = sudokuagents.const_prop(board)

print("\n Unsolved sudoku puzzle: ")
sudokuboards.Format(board)

# TEST FOR BACKTRACKING
def timer(sudoku, agent):
    t1 = perf_counter()
    if agent.solve(board,0,0): # backtracking        
        print(f"Solved Sudoku:")
        sudokuboards.Format(sudoku)

    else:
        print("No solution for this Sudoku")

    t2 = perf_counter()
    print(f' TIME TAKEN = {round(t2-t1,3)} SECONDS \n\n')
    return sudoku
timer(board, agent)

# TEST FOR DANCING LINKS
class Sudoku(board):
    def solve(self, board):
        # Solve the board, defined in agents, where the board is converted to a exact cover problem
        agent.DLX.link_nodes(board)
        solved_sudoku, sol_exist = agent.DLX.exact_sol([])
        return solved_sudoku, sol_exist

    def ECP_to_grid(self, solved_sudoku, sol_exist):
        # Reconvert Exact cover problem back to board
        if not sol_exist:
            print('No solution for the given Sudoku')
            return
        solution = [0] * 81
        for i in solved_sudoku:
            value = i.row % 9
            if value == 0:
                value = 9
            solution[(i.row - 1) // 9] = value
        self.format_board(''.join(str(i) for i in solution))

    def format_board(self, grid_str):
        """Outputs Sudoku grid in a readable format"""
        print('')
        grid = list(grid_str)
        row = list('+-------+-------+-------+')
        for index, chr in enumerate(grid):
            if index % 9 == 0:
                print(''.join(row))
                if index % 27 == 0 and index > 0:
                    print('+-------+-------+-------+')
                row = []
            if index % 3 == 0:
                row.extend(['|', ' '])
            row.extend([chr, ' '])
            if (index + 1) % 9 == 0:
                row.append('|')
            if index == len(grid_str) - 1:
                print(''.join(row))
                print('+-------+-------+-------+\n')
if __name__ == "__main__":
    board = Sudoku()
    print('Enter a sudoku puzzle in the string format')
    # IMPORTING STRING SUDOKU FROM SUDOKUBOARDS.PY
    sudoku_string = sudokuboards.string_sudoku(board)

    while sudoku_string != 'exit':
        t1 = perf_counter()
        solved_sudoku, sol_exist = board.solve(sudoku_string)
        board.ECP_to_grid(solved_sudoku, sol_exist)
        t2 = perf_counter()
        sudoku_string = "exit"    
    print(f' TIME TAKEN = {round(t2-t1,3)} SECONDS \n\n')

# TEST FOR CONSTRAINT PROPOGATION
"""
For CP, I've utilised two heuristics to obtain improved results!
These are defined below:
"""
def MRV(board):
    """
    Once all the possible values are generated, the cell with the minimum number of possible values is selected
    """
    p_values = {}  # List of possible values
    for i in range(10):
        p_values[i] = []
    for (row, col), f_values in np.ndenumerate(board.f_values):
        if f_values == 0:  # If it is an empty position
            p_values[len(board.p_values[row][col])].append((row, col)) 
    for i in range(10):
        if p_values[i]:
            return p_values[i]  # Return least remaining value
        
def degree(board, row, col):
    """
    When two or more cells have same MRV, then get degree is utilised to check which cell has most number of constraints
    Then that cell is selected using this heuristic
    Returns the number of positions affected by the current position
    """
    deg = 0 
    for i in range(9):
        if board.f_values[row][i] == 0:
            deg += 1
        if board.f_values[i][col] == 0: 
            deg += 1
    block_row = row - (row % 3)
    block_col = col - (col % 3)
    for temp_row in range(3):
        for temp_col in range(3):
            if board.f_values[temp_row + block_row][temp_col + block_col]:
                deg += 1
    return deg

def best_cell(board):
    """
    Apply the above hauristics and eliminate possibilities further to select the best cell
    Check, if MRv=1, don't apply degree
    """
    min_value_positions = MRV(board)
    if len(min_value_positions) == 1:  
        return min_value_positions[0][0], min_value_positions[0][1]
    max_r, max_c, max_d = -1, -1, 0  
    for position in min_value_positions:  
        curr_degree = degree(board, position[0], position[1])
        if curr_degree > max_d:
            max_d = curr_degree 
            max_r, max_c = position 
    return max_r, max_c

def depth_first_search(board):
    """
    Uses DFS and the above Heuristics to find a solution faster
    """
    row, col = best_cell(board) 
    values = board.p_values[row][col]
    for value in values: 
        new_state = board.gen_next_state(row, col, value)
        if new_state.is_goal():
            return new_state 
        if new_state.is_solvable():
            deep_state = depth_first_search(new_state)
            if deep_state and deep_state.is_goal():
                return deep_state 

    return None

def sudoku_solver(board):
    """
    Solves a Sudoku puzzle and returns its unique solution
    """
    if not agent.value_valid(): 
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)
    if agent.Sudoku_solved():
        return agent.f_values 
    agent.init_constraints() 
    agent = depth_first_search(agent)
    if not agent:
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)
    return agent.f_values 
