from pathlib import Path
from time import perf_counter

test_file_path = Path(__file__).parent / "test_input.txt"
real_file_path = Path(__file__).parent / "input.txt"

with open(real_file_path, "r") as f:
    grid = [line.strip() for line in f]

t1 = perf_counter()

# Find all rolls in each row and store their index. Use set for faster lookup
roll_indices = [{i for i in range(len(row)) if row[i] == "@"} for row in grid]

continue_checking = True
total_number_of_accessible_rolls = 0
while continue_checking:
    number_of_accessible_rolls = 0
    # Keep track of all indices to remove until the next run
    total_indices_to_remove = []
    for i, row in enumerate(roll_indices):
        # Use a set to remove the old indices
        indices_to_remove = set()
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
                # Add the index to the indices to remove for the row
                indices_to_remove.add(index)

        # Add all of the indices to remove for the row to the totals
        total_indices_to_remove.append(indices_to_remove)
    if number_of_accessible_rolls:
        total_number_of_accessible_rolls += number_of_accessible_rolls
        # Update each row using the indices that were found during the run
        for i, row in enumerate(roll_indices):
            row.difference_update(total_indices_to_remove[i])
    else:
        continue_checking = False

t2 = perf_counter()

print("Total number of accessible rolls: ", total_number_of_accessible_rolls)
print(f"Total time: {t2 - t1:.4f}")
