from ast import literal_eval
from functools import reduce
from itertools import combinations
from pathlib import Path
from time import perf_counter

file_path = Path(__file__).parent / "input.txt"

with open(file_path, "r") as f:
    lines = [line.strip().split() for line in f]

# The problem seems like a binary algebra problem, since the lights can be interpreted as bits being 0 or 1.
# Toggling bits between 0 or 1 can be achieved using an XOR operation which is commutative, meaning that
# a XOR b XOR a = a XOR a XOR b = 0 XOR b = b, since toggling the bits of any number twice simply results in 0.
# This means that pressing any button more than once is equal to not pressing the button at all, which means that
# the maximum number of times needed to press a button is the number of buttons available.

t1 = perf_counter()
total_presses = 0
for line in lines:
    lights = line[0].strip("[]").replace(".", "0").replace("#", "1")
    lights_integer = int(lights, 2)
    buttons = [x if isinstance((x := literal_eval(button)), tuple) else (x,) for button in line[1:-1]]
    # Convert the left-aligned index given in the buttons array to a right-aligned bit index, and then convert these
    # indices to an integer.
    integer_buttons = [sum(2 ** (len(lights) - x - 1) for x in button) for button in buttons]
    if lights_integer in integer_buttons:
        total_presses += 1
        continue
    for k in range(2, len(buttons)):
        button_combinations = combinations(integer_buttons, k)
        if any(reduce(lambda a, b: a ^ b, combination) == lights_integer for combination in button_combinations):
            total_presses += k
            break
t2 = perf_counter()
print("Min number of button presses: ", total_presses)
print(f"Total time: {t2 - t1: .4f}")
