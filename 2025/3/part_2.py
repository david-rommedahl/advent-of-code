from pathlib import Path
from time import perf_counter

test_path = Path(__file__).parent / "input.txt"

with open(test_path, "r") as f:
    banks = [line.strip() for line in f]

t1 = perf_counter()
all_numbers = []
for bank in banks:
    latest_index = -1
    bank_number = []
    for i in range(12, 0, -1):
        index = latest_index + 1
        biggest_num = 0
        if i == 1:
            selection_slice = bank[index:]
        else:
            selection_slice = bank[index : -i + 1]
        for num in selection_slice:
            if int(num) > biggest_num:
                biggest_num = int(num)
                latest_index = index
            index += 1
        bank_number.append(str(biggest_num))
    all_numbers.append(int("".join(bank_number)))
t2 = perf_counter()
print("Total joltage sum: ", sum(all_numbers))
print(f"Total time: {t2 - t1:.4f}")
