from collections import defaultdict
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


for x, y in tile_coordinates:
    rows[y].append(x)
    columns[x].append(y)

print("Number of points in rows: ", set(len(row) for row in rows.values()))
print("Number of points in columns: ", set(len(column) for column in columns.values()))
t2 = perf_counter()
print(f"Total time: {t2 - t1:.4f}")
