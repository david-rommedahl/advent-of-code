from pathlib import Path
from time import perf_counter

test_input_path = Path(__file__).parent / "test_input.txt"
real_input_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()
with open(real_input_path, "r") as f:
    diagram = [line.strip() for line in f]

start_index = diagram[0].find("S")
min_index = 0
max_index = len(diagram[0]) - 1
splitter_indices = [set(i for i in range(len(line)) if line[i] == "^") for line in diagram[1:]]

ray_indices = {start_index}
num_splits = 0
for level in splitter_indices:
    new_indices = set()
    for ray_index in ray_indices:
        if ray_index in level:
            num_splits += 1
            new_indices.update([max(min_index, ray_index - 1), min(max_index, ray_index + 1)])
        else:
            new_indices.add(ray_index)
    ray_indices = new_indices
t2 = perf_counter()
print("Total number of splits: ", num_splits)
print(f"Total time: {t2 - t1:.4f}")
