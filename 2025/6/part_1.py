from functools import reduce
from pathlib import Path
from time import perf_counter

test_input_path = Path(__file__).parent / "test_input.txt"
real_input_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()
with open(real_input_path, "r") as f:
    problem_lines = [line.split() for line in f]
    numbers, operators = list(zip(*[map(int, line) for line in problem_lines[:-1]])), problem_lines[-1]

total = 0
for i in range(len(numbers)):
    if operators[i] == "+":
        total += reduce(lambda a, b: a + b, numbers[i])
    else:
        total += reduce(lambda a, b: a * b, numbers[i])

t2 = perf_counter()
print("Grand total: ", total)
print(f"Total time: {t2 - t1:.4f}")
