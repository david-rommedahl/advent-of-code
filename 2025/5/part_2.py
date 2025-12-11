from pathlib import Path
from time import perf_counter

test_file_path = Path(__file__).parent / "test_input.txt"
real_input_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()
with open(real_input_path, "r") as f:
    fresh_ranges: list[range] = []
    while True:
        line = next(f)
        if stripped_line := line.strip():
            start, end = stripped_line.split("-")
            fresh_range = range(int(start), int(end) + 1)
            fresh_ranges.append(fresh_range)
        else:
            break

sorted_ranges = sorted(fresh_ranges, key=lambda x: x.start)
number_of_fresh_ingredients = 0
last_range: range | None = None
for current_range in sorted_ranges:
    if last_range and last_range.stop > current_range.start:
        if current_range.stop <= last_range.stop:
            continue
        current_range = range(last_range.stop, current_range.stop)
    number_of_fresh_ingredients += len(current_range)
    last_range = current_range
t2 = perf_counter()

print("Total number of fresh ingredients: ", number_of_fresh_ingredients)
print(f"Total time: {t2 - t1:.4f}")
