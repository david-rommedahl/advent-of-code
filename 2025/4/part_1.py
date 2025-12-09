from pathlib import Path
from time import perf_counter

test_file_path = Path(__file__).parent / "test_input.txt"
real_file_path = Path(__file__).parent / "input.txt"

with open(real_file_path, "r") as f:
    grid = [line.strip() for line in f]

t1 = perf_counter()

# Find all rolls in each row and store their index. Use set for faster lookup
roll_indices = [{i for i in range(len(row)) if row[i] == "@"} for row in grid]

number_of_accessible_rolls = 0
for i, row in enumerate(roll_indices):
    for index in row:
        adjacent_rolls = 0
        # Check previous row
        if i >= 1:
            adjacent_rolls += sum(x in roll_indices[i - 1] for x in (index - 1, index, index + 1))

        # Check current row
        adjacent_rolls += sum(x in row for x in (index - 1, index + 1))

        # Check next row
        if i <= len(roll_indices) - 2:
            adjacent_rolls += sum(x in roll_indices[i + 1] for x in (index - 1, index, index + 1))

        # Verify that there are less than 4 adjacent rolls
        if adjacent_rolls < 4:
            number_of_accessible_rolls += 1

t2 = perf_counter()

print("Total number of accessible rolls: ", number_of_accessible_rolls)
print(f"Total time: {t2 - t1:.4f}")
