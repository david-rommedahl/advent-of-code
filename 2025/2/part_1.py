from pathlib import Path
from time import perf_counter

with open(Path(__file__).parent / "input.txt", "r") as f:
    ranges = [tuple(map(int, range_string.split("-"))) for range_string in f.readline().split(",")]


# First solution [SLOW]
t1 = perf_counter()
invalid_id_sum = 0
for start, end in ranges:
    for number in range(start, end + 1):
        str_num = str(number)
        if (str_len := len(str_num)) % 2 == 0:
            if str_num[: str_len // 2] == str_num[str_len // 2 :]:
                invalid_id_sum += number
total_time = perf_counter() - t1
print("Sum of all invalid IDs (v1): ", invalid_id_sum)
print(f"Took: {total_time:.4f} seconds")


def get_possible_numbers(original_num):
    repeat_len = len(str(original_num)) // 2
    number_multiplier = 10 ** (repeat_len) + 1
    possible_nums = [num * number_multiplier for num in range(10 ** (max(repeat_len - 1, 0)), 10**repeat_len)]
    return possible_nums


print("\n")


t1 = perf_counter()
invalid_id_sum = 0
for start, end in ranges:
    possible_nums = set(get_possible_numbers(start)).union(get_possible_numbers(end))
    invalid_id_sum += sum(num for num in possible_nums if num in range(start, end + 1))
total_time = perf_counter() - t1
print("Sum of all invalid IDs (v2): ", invalid_id_sum)
print(f"Took {total_time:.4f} seconds")
