from pathlib import Path
from time import perf_counter
from typing import Iterable, Iterator, Sequence

file_path = Path(__file__).parent / "test_input.txt"

with open(file_path, "r") as f:
    lines = [line.strip().split() for line in f]


def dot(a: Sequence[int], b: Sequence[int]) -> int:
    """Performs the dot product between two vectors of the same length."""
    if not len(a) == len(b):
        raise ValueError("Both vectors must be of same length")
    return sum(x * y for x, y in zip(a, b))


def add(a: Sequence[int], b: Sequence[int]) -> list[int]:
    if not len(a) == len(b):
        raise ValueError("Both vectors must be of same length")
    return [x + y for x, y in zip(a, b)]


class Matrix:
    def __init__(self, rows: Iterable[Iterable[int]]) -> None:
        self.rows = [list(row) for row in rows]

    @classmethod
    def from_columns(cls, columns: Sequence[Sequence[int]]) -> Matrix:
        """Alternative constructor"""
        return cls(list(zip(*columns)))

    @property
    def columns(self) -> list[list[int]]:
        return [list(row) for row in zip(*self.rows)]

    @property
    def leading_zeros(self) -> list[int]:
        leading_zeros = []
        for row in self.rows:
            try:
                leading_zeros.append(next(i for i, x in enumerate(row) if x != 0))
            except StopIteration:
                leading_zeros.append(len(self.columns))
        return leading_zeros

    @property
    def T(self) -> Matrix:
        """Transposition method inspired by numpy"""
        return Matrix(self.columns)

    def mult(self, other: Matrix | Sequence[int]) -> Matrix | list[int]:
        """Perform multiplication between the matrix and another Matrix or vector"""
        if isinstance(other, Sequence):
            return [dot(row, other) for row in self.rows]
        elif isinstance(other, Matrix):
            return Matrix([[dot(row, column) for column in other.columns] for row in self.rows])

    def sort_on_leading_zeros(self, vector: Sequence[int] | None = None) -> Matrix | tuple[Matrix, list[int]]:
        """Sorts rows of the matrix and a provided vector based on the leading zeros in the matrix' rows."""
        if isinstance(vector, Sequence):
            matrix, b = zip(*[x for _, x in sorted(zip(self.leading_zeros, (zip(self, vector))))])
            return Matrix(matrix), list(b)
        return Matrix([row for _, row in sorted(zip(self.leading_zeros, self.rows))])

    def __iter__(self) -> Iterator[Sequence[int]]:
        for row in self.rows:
            yield row

    def __repr__(self) -> str:
        return f"[{'\n '.join(str(row) for row in self.rows)}]"


def sort_augmented_matrix(matrix: list[tuple[list[int], int]]) -> list[tuple[list[int], int]]:
    """Sorts an augmented matrix so that rows with leading zeros are lower than rows without."""
    return sorted(matrix, key=lambda row: next(i for i, x in enumerate(row[0]) if x != 0))


def reduce_to_row_echelon(matrix: Matrix, b: Sequence[int]) -> tuple[Matrix, list[int]]:
    """Takes a matrix and a solution vector and reduces the augmented matrix to row echelon form."""
    matrix, b = matrix.sort_on_leading_zeros(b)
    while True:
        # First step, check if there are more than one column with the same amount of leading zeros
        leading_zero_counts = [(sum(int(x == y) for x in matrix.leading_zeros), y) for y in matrix.leading_zeros]
        # Get the row number and the number of leading zeros for that row
        duplicate_pivot_rows = [
            (i, x[1]) for i, x in enumerate(leading_zero_counts) if (x[0] > 1 and x[1] < len(matrix.columns))
        ]
        if not duplicate_pivot_rows:
            break

        first_index, first_num_zeros = duplicate_pivot_rows[0]
        rows_to_subtract = [index for index, num_zeros in duplicate_pivot_rows[1:] if num_zeros == first_num_zeros]

        for index in rows_to_subtract:
            multiplier = next(c for c in matrix.rows[index] if c != 0)
            matrix.rows[index] = add(matrix.rows[index], [-x * multiplier for x in matrix.rows[first_index]])
            b[index] = b[index] - b[first_index] * multiplier
        matrix, b = matrix.sort_on_leading_zeros(b)
    return matrix, b


t1 = perf_counter()
# Test on first matrix
for line in lines:
    buttons = [[int(x) for x in button.strip("()").split(",")] for button in line[1:-1]]
    b = [int(x) for x in line[-1].strip("{}").split(",")]
    columns = [[1 if x in button else 0 for x in range(len(b))] for button in buttons]
    matrix = Matrix.from_columns(columns)
    print(f"Matrix:\n{matrix}")
    print("b: ", b)
    matrix, b = reduce_to_row_echelon(matrix, b)
    print(f"Augmented matrix:\n[{'\n '.join(str(x) for x in list(zip(matrix, b)))}]")
    free_variables = [i for i in range(len(matrix.columns)) if i not in matrix.leading_zeros]
    print("Free variables: ", free_variables)
t2 = perf_counter()
print(f"Total time: {t2 - t1:.4f}")
