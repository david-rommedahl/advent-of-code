from pathlib import Path
from time import perf_counter

test_file_path = Path(__file__).parent / "test_input.txt"
real_input_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()
with open(real_input_path, "r") as f:
    fresh_ranges = []
    while True:
        line = next(f)
        if stripped_line := line.strip():
            fresh_ranges.append(stripped_line)
        else:
            break
    available_ingredients = [int(line.strip()) for line in f]

fresh_ranges = [
    range(start, end + 1) for start, end in [tuple(map(lambda i: int(i), r.split("-"))) for r in fresh_ranges]
]
total_fresh_available_ingredients = sum(
    any(ingredient in fresh_range for fresh_range in fresh_ranges) for ingredient in available_ingredients
)
t2 = perf_counter()
print("Fresh, available ingredients: ", total_fresh_available_ingredients)
print(f"Total time: {t2 - t1:.4f}")
