from pathlib import Path
from time import perf_counter

test_path = Path(__file__).parent / "test_input.txt"
real_path = Path(__file__).parent / "input.txt"
with open(real_path, "r") as f:
    banks = [line.strip() for line in f]

t1 = perf_counter()
highest_joltages = []
for bank in banks:
    biggest_number = 0
    biggest_index = 0
    second_biggest_number = 0
    for i in range(len(bank) - 1):
        if (new_number := int(bank[i])) > biggest_number:
            biggest_number = new_number
            biggest_index = i
    for j in range(len(bank)):
        if (new_number := int(bank[j])) > second_biggest_number:
            if j > biggest_index:
                second_biggest_number = new_number
    highest_joltages.append(int(str(biggest_number) + str(second_biggest_number)))
t2 = perf_counter()
print("Total joltage sum: ", sum(highest_joltages))
print(f"Total time: {t2 - t1:.4f}")
