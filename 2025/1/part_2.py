from pathlib import Path

with open(Path(__file__).parent / "input.txt", "r") as f:
    input_tuples = [(line.strip()[0], int(line.strip()[1:])) for line in f if line]
    steps_list = [-steps if direction == "L" else steps for direction, steps in input_tuples]

# Dial goes from 0 to 99. The starting value is 50.
dial = 50
dial_size = 100
number_of_0 = 0
for steps in steps_list:
    starting_point = dial
    full_rotations = abs(steps) // dial_size
    dial = (dial + steps) % dial_size
    number_of_0 += full_rotations
    if dial == 0 and (abs(steps) % dial_size != 0):
        number_of_0 += 1
    elif steps > 0 and (starting_point + (steps % dial_size) > dial_size):
        number_of_0 += 1
    elif starting_point != 0 and steps < 0 and (starting_point - (abs(steps) % dial_size) < 0):
        number_of_0 += 1
print("Total number of times pointing at 0: ", number_of_0)
