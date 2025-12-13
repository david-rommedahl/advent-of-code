from functools import reduce
from itertools import combinations
from pathlib import Path
from time import perf_counter

file_path = Path(__file__).parent / "input.txt"

t1 = perf_counter()

with open(file_path, "r") as f:
    boxes = [tuple(map(int, line.strip().split(","))) for line in f]


def distance(a, b):
    return sum(map(lambda coords: (coords[0] - coords[1]) ** 2, zip(a, b))) ** 0.5


tx = perf_counter()
# select the ten shortest connections
box_pairs = sorted(combinations(boxes, r=2), key=lambda x: distance(*x))[:1000]
ty = perf_counter()

# Store the actual circuits
circuits: dict[int, set] = {}
# Store a lookup table for which circuit a box belongs to
circuit_mapping: dict[tuple[int], int] = dict()
for pair in box_pairs:
    box = next(iter(box for box in pair if box in circuit_mapping), None)
    if box is None:
        box_1, box_2 = pair
        circuit = hash(pair)
        circuits[circuit] = {box_1, box_2}
        circuit_mapping[box_1] = circuit
        circuit_mapping[box_2] = circuit
    else:
        circuit = circuit_mapping[box]
        box_2 = next(iter(_box for _box in pair if _box is not box))
        if box_2 not in circuit_mapping:
            circuits[circuit].add(box_2)
            circuit_mapping[box_2] = circuit
        else:
            circuit_2 = circuit_mapping.get(box_2)
            if circuit == circuit_2:
                continue
            circuits[circuit].update(circuits[circuit_2])
            circuit_mapping.update({b: circuit for b in circuits[circuit_2]})
            circuits.pop(circuit_2)

three_longest_circuits = reduce(lambda a, b: a * b, sorted([len(x) for x in circuits.values()], reverse=True)[:3])

t2 = perf_counter()
print("Product of the three longest circuits: ", three_longest_circuits)
print(f"Total time: {t2 - t1:.4f}")
print(f"Time to calculate pairs: {ty - tx:.4f}")
