from itertools import chain
from pathlib import Path
from time import perf_counter

with open(Path(__file__).parent / "input.txt", "r") as f:
    ranges = [tuple(map(int, range_string.split("-"))) for range_string in f.readline().split(",")]


def get_multiplier(number_len: int, num_repeats: int = 2):
    """Returns a repeat multiplier for a number.

    When the multiplier is multiplied with a number, it returns the number repeated `num_repeats` times"""
    # if num_repeats < 2:
    #     raise ValueError("Number of repeats must be more than 1")
    multiplier = 0
    for i in range(1, num_repeats):
        multiplier += 10 ** (number_len * i)
    multiplier += 1
    return multiplier


t1 = perf_counter()
max_number_length = max(len(str(num)) for num in chain.from_iterable(ranges))
# Pre-create all possible invalid IDs, based on the maximum length of the numbers in the given ranges
ids = set()
for number_len in range(2, max_number_length + 1):
    # Get the possible length of of the repetitions by finding the divisors of the number length
    possible_repeat_lengths = [
        divisor for divisor in range(1, number_len) if number_len / divisor == number_len // divisor
    ]
    for repeat_length in possible_repeat_lengths:
        num_repeats = number_len // repeat_length
        multiplier = get_multiplier(repeat_length, num_repeats)
        ids.update(multiplier * num for num in range(10 ** (repeat_length - 1), 10**repeat_length))
ids = sorted(ids)
print("Number of invalid IDs: ", len(ids))

# Sum up all invalid IDs which fall within the given ranges
invalid_id_sum = 0
for start, end in ranges:
    invalid_id_sum += sum(filter(lambda x: start <= x <= end, ids))
total_time = perf_counter() - t1
print("Total sum of invalid IDs: ", invalid_id_sum)
print(f"Total time: {total_time:.4f}")
