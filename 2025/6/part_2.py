from functools import reduce
from pathlib import Path
from time import perf_counter

test_input_path = Path(__file__).parent / "test_input.txt"
real_input_path = Path(__file__).parent / "input.txt"

# In this problem I have to keep the numbers as strings, and use the operators to figure out the spacing
t1 = perf_counter()
with open(real_input_path, "r") as f:
    problem_lines = [line.strip("\n") for line in f]
    numbers, operators = problem_lines[:-1], problem_lines[-1]

operator_indices = [i for i, operator_character in enumerate(operators) if operator_character in ("+", "*")]
# Split the lines up into individual numbers, using the fact that the first digit of every
# number has the same index as the operator which belongs to that problem that the number belongs to.
# Directly transpose the rows and columns, so that the numbers that belong to
# the same problem end up in the same inner list
individual_number_strings = [
    [
        line[operator_indices[index] : operator_indices[index + 1] - 1]
        if (index < len(operator_indices) - 1)
        else line[operator_indices[index] :]
        for line in numbers
    ]
    for index in range(len(operator_indices))
]

# Here we again transpose the strings representing the individual numbers, so that ["123", " 16", "  1"]
# ends up like ["  1", "21 ", "361"], which when converting to integers ends up being [1, 21, 361], which
# is the format we need
individual_numbers = list([int("".join(y)) for y in zip(*x)] for x in individual_number_strings)
total = 0
for i, operator in enumerate(operators.split()):
    if operator == "+":
        total += reduce(lambda a, b: a + b, individual_numbers[i])
    else:
        total += reduce(lambda a, b: a * b, individual_numbers[i])
t2 = perf_counter()

print("Grand total: ", total)
print(f"Total time: {t2 - t1:.4f}")
