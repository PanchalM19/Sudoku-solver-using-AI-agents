# from sudokuboards import easy, Format, medium,difficult,vDifficult
# import time
from math import inf
import numpy as np

class backtracking():
    def valid_move(self, board, row, col, value):
        """
        Check for the num in row, column and 3x3 grid
        """
        if value in board[row]:
            return False
        if value in [board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == value:
                    return False #

        return True

    def solve(self, board, row, col):
        """
        Solve sudoku using recursion and backtracking
        """
        if col == 9:
            if row == 8:
                return True #traverse through entire grid, if last cell is reached, return solution
            row += 1 #Increment row
            col = 0 #Reset colum, and traverse next column
        if board[row][col] > 0: #If the cell value is not 0, run solve fucntion
            return self.solve(board, row, col + 1) # over the next column
        for i in range(1,10):
            if self.valid_move(board, row, col, i):
                board[row][col] = i 
                if self.solve(board, row, col + 1):
                    return True # Provide solution recursively
            board[row][col] = 0 # backtrack to the last value that satisfies the constraint and try different value and return 0 for current cell
        return False


class knuth():

    class Node(object):
        """
        This is used for creating a doubly linked list. It will be used to convert Sudoku to exact cover problem
        """
        def __init__(self, column, row):
            self.column = column
            self.row = row
            self.up, self.down, self.left, self.right = self, self, self, self

    class initialnodes(Node):
        def __init__(self, id):
            knuth.Node.__init__(self, self, id)
            self.row_count = 0

    class DLX(object):
        def __init__(self):
            self.root = knuth.initialnodes(0)

        def link_nodes(self, grid_str):
            """
            Converting Sudoku to Exact Cover
            """
            root = self.root
            cols = [root]
            for i in range(324): # Linking all the cells by using the init function defined above
                c = knuth.initialnodes(i + 1)
                c.right = root
                c.left = root.left
                root.left.right = c
                root.left = c
                cols.append(c)
            row_const = 81 # Defining the sudoku constraints and rules
            col_const = 162
            grid_const = 243
            row_rule = lambda x, k: row_const + (x // 9) * 9 + k
            col_rule = lambda x, k: col_const + (x % 9) * 9 + k
            grid_rule = lambda x, k: grid_const + (x // 27) * 27 + (x % 9) // 3 * 9 + k
            row_no = lambda x, k: x * 9 + k

            def col_link(value):
                """
                Link all columns
                """
                c_n = value.column
                c_n.row_count += 1
                value.down = c_n
                value.up = c_n.up
                c_n.up.down = value
                c_n.up = value

            def row_link(x, k):
                """
                Link all rows
                """
                cell_node = knuth.Node(cols[x + 1], row_no(x, k))
                row_node = knuth.Node(cols[row_rule(x, k)], row_no(x, k))
                col_node = knuth.Node(cols[col_rule(x, k)], row_no(x, k))
                box_node = knuth.Node(cols[grid_rule(x, k)], row_no(x, k))
                cell_node.right, cell_node.left = row_node, box_node
                row_node.right, row_node.left = col_node, cell_node
                col_node.right, col_node.left = box_node, row_node
                box_node.right, box_node.left = cell_node, col_node
                col_link(cell_node)
                col_link(row_node)
                col_link(col_node)
                col_link(box_node)
            for i, j in enumerate(grid_str):
                if j == '.':
                    for k in range(9):
                        row_link(i, k + 1)
                else:
                    row_link(i, ord(j) - 48)

        def eliminate_cons(self):
            """
            Eliminates possibilities based on constraints
            """
            col = None
            i = self.root.right
            constraints = inf
            while i != self.root:
                if i.row_count < constraints:
                    col = i
                    constraints = i.row_count
                i = i.right
            return col

        def find_cover(self, col):
            """
            Exact cover logic is implemented over here.
            The rows that interest the given column "col" is removed or "covered"
            """
            col.right.left = col.left
            col.left.right = col.right
            i = col.down
            while i != col: #Unlinks the rows that intersect "col"
                j = i.right
                while j != i:
                    j.down.up = j.up
                    j.up.down = j.down
                    j.column.row_count -= 1
                    j = j.right
                i = i.down

        def check_uncover(self, col):
            i = col.up
            while i != col:
                j = i.left
                while j != i:
                    j.down.up = j
                    j.up.down = j
                    j.column.row_count += 1
                    j = j.left
                i = i.up
            col.right.left = col
            col.left.right = col

        def exact_sol(self, solution):
            """
            Look for the exact solution
            """
            if self.root == self.root.right:
                return solution, True
            c = self.eliminate_cons()
            self.find_cover(c)
            i = c.down
            while i != c:
                solution.append(i)
                j = i.right
                while j != i:
                    self.find_cover(j.column)
                    j = j.right
                solution, found = self.exact_sol(solution)
                if found:
                    return solution, True
                i = solution.pop()
                c = i.column
                j = i.left
                while j != i:
                    self.check_uncover(j.column)
                    j = j.left
                i = i.down
            self.check_uncover(c)
            return solution, False



class const_prop():
    def __init__(self, f_values):
        self.f_values = f_values
        self.values = np.empty(shape=(9, 9), dtype=list)

    def init_constraints(self):
        """
        Select "values" that are in line with the constraints
        """
        for row in range(9):
            for col in range(9):
                self.values[row][col] = []  
                if self.f_values[row][col] == 0: # Check if cell is vacant
                    possible_values = []  # Select "value"

                    # Check the constraints
                    for value in range(1, 10):
                        if self.value_valid(row, col, value):
                            possible_values.append(value)  # If "value" is valid, add at the cell location
        return

    def value_valid(self, row, col, value):
        """
        Here we test if the "values" are as per Sudoku constraints or not
        """
        if value == 0:
            return True  # Valid        
        for i in range(9): # Check in row,col and 3x3 grid
            if self.f_values[i][col] == value and i != row:
                return False 
            if self.f_values[row][i] == value and i != col:
                return False 
        grid_r = row - (row % 3)
        grid_c = col - (col % 3)
        for row in range(3):
            for col in range(3):
                if value == self.f_values[grid_r + row][grid_c + col] and grid_r + row != row and grid_c + col != col:
                    return False 
        return True

    def check_clues(self):
        """
        Check the initial Sudoku board provided
        """
        for (row, col), value in np.ndenumerate(self.f_values): 
            if not self.value_valid(row, col, value): 
                return False
        return True

    def baord_sol(self):
        """
        Check if one solution exists. Each valid Sudoku board (board that has passed "check_clues" fucntion) should have only one unique solution
        """
        for row, col in np.ndindex(9, 9):
            if len(self.values[row][col]) < 1 and self.f_values[row][col] == 0:
                return False
        return True

    def Sudoku_solved(self):
        """
        Sudoku if solved, if no "values" in any cell are 0
        """
        if 0 in self.f_values:
            return False
        return True

    def unique_value(self):
        """
        If it is vacant and has only one possible value append it
        """
        s_value = []
        for row in range(9):
            for col in range(9):
                if len(self.values[row][col]) == 1 and self.f_values[row][col] == 0:
                    s_value.append((row, col))
        return s_value

    def check_const(self, row, col, value):
        """
        Enter "values" and check if all constraints are satisfied
        """
        c_values = [self.values[i][col] for i in range(9)]
        for i in c_values:
            if value in i:
                i.remove(value)
        r_values = self.values[row]
        for i in r_values:
            if value in i:
                i.remove(value)
        grid_r = row - (row % 3)
        grid_c = col - (col % 3)
        for row in range(3):
            for col in range(3):
                if value in self.values[grid_r + row][grid_c + col]:
                    self.values[grid_r + row][grid_c + col].remove(value)
        return

    def copy_state(self):
        """
        Numpy (np) has built-in ".copy" function
        """
        cell_value = const_prop(np.ndarray.copy(self.f_values)) 
        for (row, col), values in np.ndenumerate(self.values):
            cell_value.possible_values[row][col] = values[:] 
        return cell_value 

    def solution(self, row, col, value):
        """
        This function will utilise the above function to give the possible values! and return the solved sudoku
        """
        cell_value = self.copy_state() 
        cell_value.final_values[row][col] = value
        cell_value.possible_values[row][col] = []
        cell_value.update_constraints(row, col, value) #Apply constraints and check if value is valid
        # unique_cell_value = cell_value.unique_value()
        while True:
            updated = False
            for r in range(9):
                for c in range(9):
                    if not cell_value.final_values[r][c]:  # Cell is empty
                        possible_values = cell_value.possible_values[r][c]
                        if len(possible_values) == 1:  # Only one possible value for the cell
                            cell_value.final_values[r][c] = possible_values[0]
                            cell_value.possible_values[r][c] = []
                            cell_value.update_constraints(r, c, cell_value.final_values[r][c])
                            updated = True
            if not updated:  # If no more unique values found, exit loop
                break
        return cell_value