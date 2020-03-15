"""Helper function for multi-armed bandit problem."""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
from abc import ABC, abstractmethod


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


class Agent(ABC):
    """Abstract class for an agent."""

    @abstractmethod
    def __init__(self, env: TestBed, verbose: bool, **kwargs):
        """Define the environment the agent will be in, and values."""
        self.env = env
        self.verbose = verbose
        self.arm_values = None  # values for each arm, same shape as arm counts
        self.arm_counts = None  # number of pulls for each arm
        self.arms_history = None  # histry of arms pulled for each step
        self.values_history = None

        self.simulation_finished = False

        self.current_arm = None
        self.current_value = None

    def init_values(self, value: float):
        """Initialize the value estimates."""
        self.simulation_finished = False
        self.current_step = 0
        self.arm_counts = np.zeros(self.env.number_of_arms)

        if value is not None:  # uniform initial values
            self.arm_values = np.array(
                [value for _ in range(self.env.number_of_arms)])
        else:  # it is None, then random values
            self.arm_values = np.random.normal(
                size=self.env.number_of_arms)

    def update_logs(self, s: int):
        """Update the logs at step s."""
        self.values_history[s] = self.current_value
        self.arms_history[s] = self.current_arm

    @abstractmethod
    def update_values(self):
        """Update the values estimates."""
        raise NotImplementedError

    @abstractmethod
    def take_single_step(self):
        """From the current value estimate, take an action."""
        raise NotImplementedError

    def run(self, steps: int):
        """Run the simulation."""
        if self.arm_values is None:
            raise('Please initialize the agent.')
        if self.simulation_finished:
            return

        self.arms_history = -1 * np.ones(steps)
        self.values_history = np.zeros(steps)
        for s in tqdm(range(steps), desc='Agent running'):
            self.take_single_step()

            self.arm_counts[self.current_arm] += 1
            self.update_values()
            self.update_logs(s)

        self.simulation_finished = True
        return


class GreedyAgent(Agent):
    """Greedy policy."""

    def __init__(self, env: TestBed, verbose: bool, **kwargs):
        """Put the agent in an environment."""
        super().__init__(env=env, verbose=verbose)

    def pick_largest(self) -> int:
        """Pick the arm that has largest value. Breaks tie randomly."""
        return np.random.choice(
            np.flatnonzero(self.arm_values == self.arm_values.max()))

    def update_values(self):
        """Update the values estimates."""
        # sample average
        self.arm_values[self.current_arm] += \
            ((self.current_value - self.arm_values[self.current_arm]) /
             self.arm_counts[self.current_arm])

    def take_single_step(self):
        """Update the values estimates."""
        self.current_arm = self.pick_largest()
        self.current_value = self.env.emit(self.current_arm)


if __name__ == '__main__':
    print('Making the environment...', end=' ')
    k = 10
    bed = TestBed(k)
    print('Environment made.')
    print(f"Number of arms: {bed.number_of_arms}")
    print(f"Means of the arms: {bed.mus}")
    print(f"Stds of the arms: {bed.stds}")
    print(f"The best arm is {bed.best_arm}")
    test_arm = 5
    print("Emits a value from {} as: {:5.3f}"
          .format(test_arm, bed.emit(test_arm)))
    # bed.visualize()

    print("Greedy angent")
    GA = GreedyAgent(bed, verbose=True)
    GA.init_values(0.0)
    # run simulation
    GA.run(100)
    print('value history: ', GA.values_history)
    print('arm history: ', GA.arms_history)
    print('arm counts: ', GA.arm_counts)
    print('arm values: ', GA.arm_values)
