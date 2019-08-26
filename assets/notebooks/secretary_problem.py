"""secretary problem
"""
import numpy as np

from typing import List
from datetime import datetime
from pathos.multiprocessing import ProcessingPool as Pool


class Simulation:
    """Look-then-leap simulations.
    """

    def __init__(self, candidates: List[int], threshold: float = 0.3):
        """
        Args:
            candidates: List of incoming candidates, represented by their
                (hidden) rankings. The higher the better.
            threshold (float): Proportion of `look` period. 0.3 means one will
                look 30% of the total candidates before leap.
        """

        self.candidates = candidates
        assert(0. < threshold < 1.)
        if not len(self.candidates) == len(set(self.candidates)):
            raise ValueError("Candidate should have unique rankings.")

        self.num_candidates = len(self.candidates)
        self.num_looks = int(threshold * self.num_candidates) + 1
        self.true_best = np.min(self.candidates)
        self.selected = None

    def run(self):
        """Simulate the interview process.
        """
        self.best_so_far = np.min(self.candidates[:self.num_looks])

        for i in self.candidates[self.num_looks:]:
            self.selected = i
            if i < self.best_so_far:
                break  # we are done!

    def evaluate(self):
        """Returns True if we do get the best candidate.
        """
        if self.selected is None:  # be careful of 0!
            raise ValueError("Please run the simulation first.")

        if self.selected == self.true_best:
            return True
        elif self.selected > self.true_best:
            return False
        else:
            raise RuntimeError("WTF?")


class Trials:
    """Runs multiple trails of the simulation.
    """
    def __init__(self, n_trials: int = 100, **kwargs):
        """Setting a single trial.
        """
        self.n_trials = n_trials
        self.n_jobs = kwargs.get('n_jobs', 10)
        self.threshold = kwargs.get('threshold', 100)
        self.n_candidates = kwargs.get('n_candidates', 100)
        self.results = []

    def single_run(self, x):
        np.random.seed(datetime.now().microsecond)
        candidates = np.random.permutation(self.n_candidates)
        S = Simulation(candidates, self.threshold)
        S.run()

        return S.evaluate()

    def run(self):
        """Runs all trials in mp fashion.
        """
        self.results = Pool(self.n_jobs).map(
            self.single_run,
            range(self.n_trials))


if __name__ == '__main__':

    n_trials = 10000
    n_candidates = 1000
    threshold = 0.37

    T = Trials(n_trials=n_trials,
              n_candidates=n_candidates,
              threshold=threshold,
              n_jobs=12)
    T.run()

    print("With {0} as the look-then-leap threshold, the chance to get the"
          " best candidate is {1:.2%}".format(threshold, np.mean(T.results)))
