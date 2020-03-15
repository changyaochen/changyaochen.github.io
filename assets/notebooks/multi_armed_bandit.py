"""Helper function for multi-armed bandit problem."""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class TestBed:
    """The environment."""

    def __init__(self, k: int, random_seed: int = 42, **kwargs):
        """Initialize the environment as k normal distributions."""
        self.random_seed = random_seed
        np.random.seed(self.random_seed)
        self.number_of_arms = k
        self.mus = np.random.normal(loc=0., scale=1., size=k)
        self.stds = [1. for _ in range(k)]
        self.best_arm = np.argmax(self.mus)
        self.distributions = pd.DataFrame()

    def emit(self, arm_idx: int) -> float:
        """Emit a sample from a given arm."""
        assert 0 <= arm_idx < self.number_of_arms
        return np.random.normal(
            loc=self.mus[arm_idx],
            scale=self.stds[arm_idx])

    def visualize(self):
        """Visualize the distribution of the arms, with help of pandas."""
        n_samples = 1000
        values = []
        idx = []
        if len(self.distributions) == 0:
            for i in range(self.number_of_arms):
                idx.extend([i] * n_samples)
                values.extend(np.random.normal(
                    loc=self.mus[i],
                    scale=self.stds[i],
                    size=n_samples))
            # make the dataframe for plotting
            self.distributions = pd.DataFrame(
                data={
                    'arm_index': idx,
                    'value': values},
            )

        # plot
        sns.set(font_scale=1.2)
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        sns.violinplot(
            x='arm_index', y='value', data=self.distributions,
            inner=None)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    bed = TestBed(10)
    print(f"Number of arms: {bed.number_of_arms}")
    print(f"Means of the arms: {bed.mus}")
    print(f"Stds of the arms: {bed.stds}")
    print(f"The best arm is {bed.best_arm}")
    bed.visualize()
