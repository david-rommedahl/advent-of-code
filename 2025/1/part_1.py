from pathlib import Path

with open(Path(__file__).parent / "input.txt", "r") as f:
    input_tuples = [(line.strip()[0], int(line.strip()[1:])) for line in f if line]
    steps_list = [-steps if direction == "L" else steps for direction, steps in input_tuples]

# Dial goes from 0 to 99. The starting value is 50.
dial = 50
dial_size = 100
number_of_0 = 0
for steps in steps_list:
    dial = (dial + steps) % dial_size
    number_of_0 += int(dial == 0)
print(number_of_0)
