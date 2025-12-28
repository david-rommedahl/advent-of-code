from functools import reduce
from itertools import combinations
from pathlib import Path
from time import perf_counter

from matplotlib import pyplot as plt

file_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()

with open(file_path, "r") as f:
    tile_coordinates = list(tuple(int(coord) for coord in line.strip().split(",")) for line in f)


def on_border(
    point: tuple[int, int],
    horizontal_lines: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]],
    vertical_lines: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]],
):
    x, y = point
    if horizontal := horizontal_lines.get(y):
        if any(line[0][0] <= x <= line[1][0] for line in horizontal):
            return True
    if vertical := vertical_lines.get(x):
        if any(line[0][1] <= y <= line[1][1] for line in vertical):
            return True
    return False


def raycast(point: tuple[int, int], horizontal_lines: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]]) -> bool:
    """Function which checks if a point is within a polygon by using raycasting.

    This implementation checks if a point is inside the polygon by casting a ray directly upward.

    Returns:
        True if the point is inside the polygon.
    """
    x, y = point
    lines_above = []
    for k, v in horizontal_lines.items():
        if k > y:
            lines_above.extend(v)
    return sum(line[0][0] < x + 0.5 < line[1][0] for line in lines_above) % 2 == 1


def length(*coords):
    if len(coords) != 2:
        raise ValueError("Need two values")
    return abs(reduce(lambda a, b: a - b, coords)) + 1


def get_reverse_points(*points, x_mapping, y_mapping):
    return tuple((x_mapping[x], y_mapping[y]) for x, y in points)


def area(a, b):
    x_coords, y_coords = zip(a, b)
    x_length = length(*x_coords)
    y_length = length(*y_coords)

    return x_length * y_length


def all_points_in_rectangle_in_polygon(a, b, outside_points: set[tuple[int, int]]) -> bool:
    xs, ys = zip(a, b)
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            if (x, y) in outside_points:
                return False
    return True


x_coords, y_coords = zip(*tile_coordinates)
x_mapping = {x: i for i, x in enumerate(sorted(set(x_coords)), start=1)}
x_reverse = {v: k for k, v in x_mapping.items()}

y_mapping = {y: i for i, y in enumerate(sorted(set(y_coords)), start=1)}
y_reverse = {v: k for k, v in y_mapping.items()}

compressed_coordinates = [(x_mapping[x], y_mapping[y]) for x, y in tile_coordinates]
line_segments = [
    line for i in range(len(compressed_coordinates)) if len(line := tuple(compressed_coordinates[i : i + 2])) == 2
]
line_segments.append((compressed_coordinates[-1], compressed_coordinates[0]))

horizontal_lines = dict()
vertical_lines = dict()
for line in line_segments:
    if line[0][0] == line[1][0]:
        sorted_line = tuple(sorted(line, key=lambda x: x[1]))
        if vertical_lines.get(line[0][0]):
            vertical_lines[line[0][0]].append(sorted_line)
        else:
            vertical_lines[line[0][0]] = [sorted_line]
    else:
        sorted_line = tuple(sorted(line, key=lambda x: x[0]))
        if horizontal_lines.get(line[0][1]):
            horizontal_lines[line[0][1]].append(sorted_line)
        else:
            horizontal_lines[line[0][1]] = [sorted_line]

# Flood fill the shape, to get all points which are outside of our polygon
outside_points = {
    (i, j)
    for i in range(0, max(vertical_lines) + 2)
    for j in range(0, max(horizontal_lines) + 2)
    if not (on_border((i, j), horizontal_lines, vertical_lines) or raycast((i, j), horizontal_lines))
}

# Now we are going to get all point combinations
coordinate_combinations = combinations(compressed_coordinates, 2)
max_area = 0
best_comb = ()
for a, b in coordinate_combinations:
    reverse_points = get_reverse_points(a, b, x_mapping=x_reverse, y_mapping=y_reverse)
    if (new_area := area(*reverse_points)) > max_area:
        if not all_points_in_rectangle_in_polygon(a, b, outside_points):
            continue
        max_area = new_area
        best_comb = reverse_points
t2 = perf_counter()
print(f"Total time: {t2 - t1:.4f}")
print("Best Area: ", max_area)
print("Best comb: ", best_comb)

# Illustration of the shape
fig, (ax1, ax2) = plt.subplots(1, 2)
for line in line_segments:
    ax1.plot(*zip(*line), c="b")

ax2.scatter(*zip(*outside_points), marker=".", c="r")
plt.show()
