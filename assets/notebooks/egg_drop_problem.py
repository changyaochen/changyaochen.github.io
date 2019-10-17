"""Egg drop problem."""
from copy import deepcopy
from math import ceil, sqrt, inf
from argparse import ArgumentParser


class EggDrop:
    """Run dynamic programming routine to solve egg drop problem."""

    def __init__(
        self,
        n: int,
        e: int):
        """Initialize problem setting.

        Args:
            n (int): Total number of floors.
            e (int): Total number of eggs.
        """
        if n < 0:
            raise ValueError("Number of floors should be positive.")
        if e < 0:
            raise ValueError("Number of eggs should be positive.")
        self.n = n
        self.e = e
        self.result = 0

        return None

    def _two_eggs(self, n):
        """Calculate the solution with 2 eggs case."""
        return ceil(0.5 * (-1 + sqrt(1 + 8 * n)))

    def run(self):
        """Run the calculations."""
        # first some edge cases
        if self.n == 0:
            return self.result
        if self.n == 1:
            self.result = 1
            return self.result
        if self.e == 1:
            self.result = self.n
            return self.result
        if self.e == 2:
            self.result = self._two_eggs(self.n)
            return self.result

        # real calculations
        else:
            # initialize the previous solution
            self.prev_solutions = {0: 0, 1: 1}
            for x in range(2, self.n + 1):
                self.prev_solutions[x] = self._two_eggs(x)

            # loop through number of eggs
            for current_e in range(self.e - 2):
                self.current_solutions = {0: 0, 1: 1}
                for current_n in range(2, self.n + 1):
                    current_min = inf
                    for k in range(2, current_n):
                        # k is the floor where we drop the first egg
                        current_min = min(
                            current_min,
                            1 + max(
                                self.prev_solutions[k - 1],  # egg breaks
                                self.current_solutions[current_n - k]  # egg doesn't break
                            )
                        )
                    self.current_solutions[current_n] = current_min
                self.prev_solutions = deepcopy(self.current_solutions)

            self.solution = self.current_solutions[self.n]

            return self.solution


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Pass arguments for the egg drop problem.')
    parser.add_argument(
        '-n',
        help='Number of floors',
        type=int,
        dest='n',
        )
    parser.add_argument(
        '-e',
        help='Number of eggs',
        type=int,
        dest='e',
        )
    args = parser.parse_args()

    S = EggDrop(n=args.n, e=args.e)
    print(S.run())
    # print(S.prev_solutions)
