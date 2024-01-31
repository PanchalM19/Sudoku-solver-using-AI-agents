# Sudoku-solver-using-AI-agents

Dive into the intricacies of Sudoku puzzles, examining varying difficulty levels and implementing algorithms on a range of boards:

## Sudoku Boards:
* Easy Puzzles (36 Clues): Offering a user-friendly experience with a significant grid portion filled, these puzzles involve straightforward reasoning and simple elimination.
* Medium Puzzles (30 Clues): Elevating the challenge, these puzzles demand more sophisticated techniques like locating concealed singles or employing intricate logical inferences.
* Difficult Puzzles (25 Clues): Testing advanced solving skills, these puzzles require strategies such as Swordfish or X-Wing, emphasizing complex logical reasoning.

Additionally, the project takes on some of the world's most challenging Sudoku problems:

* AI Escargot (22 Clues): Dubbed the "world's hardest Sudoku," this puzzle challenges solvers with minimal initial clues, necessitating advanced logic and techniques.
* Arto Inkala (21 and 22 Clues): Crafted by Finnish mathematician Arto Inkala, these puzzles are renowned for extreme difficulty, featuring very few initial clues but solvable through logic.
* Steering Wheel (19 Clues): Ranked among the toughest Sudokus, this puzzle with 19 initial clues poses a formidable challenge.
* Blonde Platine (21 Clues): With 21 initial clues, this puzzle stands as one of the most challenging Sudokus, requiring intricate strategies for successful completion.

## Sudoku Agents:

This project explores the application of various algorithms to solve Sudoku puzzles, focusing on three distinct approaches: Backtracking, Knuth’s Algorithm X (Dancing Links), and Constraint Propagation. Here's a detailed look at each algorithm:

### Backtracking:
Utilizes a cleverly optimized version of brute force, systematically exploring potential solutions.
Employs recursive algorithms to check the correctness of solutions at each step, preventing the generation of invalid recursion subtrees. A timer ensures an upper limit on solving time, enhancing efficiency.
Results: Successfully solved almost all puzzles within milliseconds. The Steering Wheel puzzle, with added countermeasures, was the only exception due to the imposed time limit.

### Knuth’s Algorithm X (Dancing Links):
Developed by Prof. Donald Knuth, this algorithm efficiently explores solution space through dancing links, a doubly linked data structure.
Tackles Sudoku as an exact cover problem, methodically covering constraints and reducing the search space with meticulous backtracking.
Results: Achieved swift solutions for all puzzles within milliseconds, aligning with expected outcomes. The algorithm demonstrates promise for larger Sudoku puzzles.

### Constraint Propagation:
Initializes the grid, validating its correctness, and populates empty cells with possible values through simple elimination.
Applies constraint propagation to iteratively reduce possibilities for each cell based on initial clues, resorting to depth-first search and backtracking if needed.
Heuristics: Introduced Minimum-Remaining-Values (MRV) and Degree heuristics for variable ordering, significantly improving runtime performance.

