from pathlib import Path
from time import perf_counter

test_input_path = Path(__file__).parent / "test_input.txt"
real_input_path = Path(__file__).parent / "input.txt"

# The second part of the problem is a binary combinatorics problem.
# Each splitter is a binary choice, where the ray can go either left or right.
# I think that the solution is to find a way to represent the problem using bits.

# As an example, let's consider this smaller version of the problem:

# .......S.......
# .......^.......
# ......^.^......


# The first split is a binary one, meaning that the number of choices here could be represented by one bit.
# After this, the ray will hit either one of the nextd splitters. This will add another bit to the possibilities.
# That means that the total number of possible worlds will be represente by two bits in this case, which will result in 2^2 possible worlds.
# If we add another layer on the problem:

# .......S.......
# .......^.......
# ......^.^......
# .....^.^.^.....

# In this case, once we get to the second level there are four different possibilities. Each one of those possibilities will end up with two new
# possibilities, which adds another bit to the problem. This gives us a total of 2^3 = 8 different timelines.

# Let's look at one final level

# .......S.......
# .......^.......
# ......^.^......
# .....^.^.^.....
# ....^.^...^....

# This is slightly different, since 4 out of the 6 possible directions in the previous level result in two new choices, but for two of the
# six possible directions, there is no split. That means that we can't describe this with just adding another bit to the problem. Once we get to this level, the
# number of possible paths was 2^3.

# I'm starting to think we can't do it this way, but that the best way to solve it might be using a depth-first binary tree search.
# Let's consider all of the splitters nodes in a binary tree. I will still represent them as their indices. Nope, the recursive solution is too slow.
# Back to the drawing board.

t1 = perf_counter()
with open(test_input_path, "r") as f:
    diagram = [line.strip() for line in f]

start_index = diagram[0].find("S")
global min_index
global max_index
global number_of_paths
global function_calls

min_index = 0
max_index = len(diagram[0]) - 1
number_of_paths = 0
function_calls = 0


def recursive_depth_first_traversal(node_index: int, remaining_levels: list[set[int]]) -> int:
    """This function gets the job done, but it is way too slow for the task."""
    global min_index
    global max_index
    global number_of_paths
    global function_calls
    function_calls += 1

    if not remaining_levels:
        number_of_paths += 1
        return
    if node_index in remaining_levels[0]:
        for new_index in (node_index - 1, node_index + 1):
            if max_index < new_index or new_index < min_index:
                # Make sure that we don't go out of bounds (even though that does not happen in our data)
                continue
            recursive_depth_first_traversal(new_index, remaining_levels[1:])
    else:
        recursive_depth_first_traversal(node_index, remaining_levels[1:])


# Now our splitter indices becomes `nodes`
splitter_indices = list(filter(None, [set(i for i in range(len(line)) if line[i] == "^") for line in diagram[1:]]))
# What we're looking for is the total number of paths that the ray could take


def test_counter(start_index: int, splitter_indices: list[set[int]]):
    ray_indices = [start_index]
    timelines = 1
    for level in splitter_indices:
        new_ray_indices = []
        timelines += sum(index in level for index in ray_indices)
        for index in ray_indices:
            if index in level:
                new_ray_indices.extend([index - 1, index + 1])
            else:
                new_ray_indices.append(index)
        ray_indices = new_ray_indices
    return timelines


print(max(len(x) for x in splitter_indices))
number_of_timelines = test_counter(start_index, splitter_indices)
t2 = perf_counter()
# recursive_depth_first_traversal(start_index, splitter_indices)
# print("Total number of paths: ", number_of_paths)
# print("Number of function calls: ", function_calls)
print(f"Total time: {t2 - t1:.4f}")
print("Number of timelines: ", number_of_timelines)
