from collections import defaultdict
from functools import reduce
from itertools import combinations
from pathlib import Path
from time import perf_counter

file_path = Path(__file__).parent / "test_input.txt"

t1 = perf_counter()

with open(file_path, "r") as f:
    tile_coordinates = list(
        sorted((tuple(int(coord) for coord in line.strip().split(",")) for line in f), key=lambda x: (x[1], x[0]))
    )

rows = defaultdict(list)
columns = defaultdict(list)


def is_on_border(point: tuple[int, int]) -> bool:
    x, y = point
    if column := columns.get(x):
        if min(column) <= y <= max(column):
            if len(column) == 4:
                if column[1] < y < column[3]:
                    return False
            return True
    if row := rows.get(y):
        if min(row) <= x <= max(row):
            if len(row) == 4:
                if row[1] < x < row[3]:
                    return False
            return True
    return False


def ray_cast(point: tuple[int, int]) -> bool:
    """Counts how many borders a ray starting at a point and going straight up would cross."""
    x, y = point
    rows_above = [rows[row] for row in rows if row < y]
    num_intersections = 0
    for row in rows_above:
        line_segments = [segment for i in range(0, len(row), 2) if (segment := row[i : i + 2])]
        for start, end in line_segments:
            if start < x < end:
                num_intersections += 1
    return num_intersections % 2 == 1


def check_point(point: tuple[int, int]) -> bool:
    return is_on_border(point) or ray_cast(point)


def length(*coords):
    if len(coords) != 2:
        raise ValueError("Need two values")
    return abs(reduce(lambda a, b: a - b, coords)) + 1


def area(a, b):
    x_coords, y_coords = zip(a, b)
    x_length = length(*x_coords)
    y_length = length(*y_coords)

    return x_length * y_length


for x, y in tile_coordinates:
    rows[y].append(x)
    columns[x].append(y)

point_combinations = combinations(tile_coordinates, 2)
valid_combinations = []
for comb in point_combinations:
    a, b = comb
    c_d = (a[0], b[1]), (b[0], a[1])
    if all(check_point(p) for p in c_d):
        valid_combinations.append(comb)
area_comb = [(x, area(*x)) for x in valid_combinations]
max_area = max(area_comb, key=lambda x: x[1])
t2 = perf_counter()
print("Max area: ", max_area)
print(f"Total time: {t2 - t1:.4f}")
