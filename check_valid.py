import numpy as np

def main():
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard', 'extreme']
    master = time.process_time()
    for difficulty in difficulties:
        solutions = np.load(f"data/{difficulty}_solution.npy")

        print(difficulty)
        for i in range(len(solutions)):
            ng = np.sum(solutions[i])
            if ng < 0:
                print(f"-1")
            else:
                print(f"1")

main()
