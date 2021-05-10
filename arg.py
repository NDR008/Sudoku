import numpy as np
solutions = np.load(f"data/hard_solution.npy")
sudokus = np.load(f"data/hard_puzzle.npy")
counter = 0
for solution in solutions:
    print(counter)
    print()
    print(solution)
    print()        
    print(sudokus[counter])
    print()
    print()
    counter = counter + 1
    