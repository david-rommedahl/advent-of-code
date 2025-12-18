from functools import reduce
from itertools import combinations
from pathlib import Path
from time import perf_counter

file_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()

with open(file_path, "r") as f:
    tile_coordinates = list(
        sorted((tuple(int(coord) for coord in line.strip().split(",")) for line in f), key=lambda x: (x[1], x[0]))
    )


def length(*coords):
    if len(coords) != 2:
        raise ValueError("Need two values")
    return abs(reduce(lambda a, b: a - b, coords)) + 1


def area(a, b):
    x_coords, y_coords = zip(a, b)
    x_length = length(*x_coords)
    y_length = length(*y_coords)

    return x_length * y_length


coord_combinations = combinations(tile_coordinates, 2)
max_area = max(area(*x) for x in coord_combinations)
t2 = perf_counter()

print("Max are: ", max_area)
print(f"Total time: {t2 - t1:.4f}")
