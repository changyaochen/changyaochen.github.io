"""Helper function for multi-armed bandit problem."""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
from abc import ABC, abstractmethod


class TestBed:
    """The environment."""

    def __init__(self, num_arms: int, random_seed: int = 42, **kwargs):
        """Initialize the environment as k normal distributions."""
        self.random_seed = random_seed
        np.random.seed(self.random_seed)
        self.num_arms = num_arms
        self.mus = np.random.normal(loc=0., scale=1., size=self.num_arms)
        self.stds = [1. for _ in range(self.num_arms)]
        self.best_arm = np.argmax(self.mus)
        self.distributions = pd.DataFrame()

    def emit(self, arm_idx: int) -> float:
        """Emit a sample from a given arm."""
        assert 0 <= arm_idx < self.num_arms
        return np.random.normal(
            loc=self.mus[arm_idx],
            scale=self.stds[arm_idx])

    def describe(self):
        """Describe basic information about the testbed."""
        tqdm.write('=====\nDetails about the testbed:')
        tqdm.write(f"Number of arms: {self.num_arms}")
        tqdm.write(f"Means of the arms: {self.mus}")
        tqdm.write(f"Stds of the arms: {self.stds}")
        tqdm.write(f"The best arm is {self.best_arm}")

    def visualize(self):
        """Visualize the distribution of the arms, with help of pandas."""
        n_samples = 1000
        values = []
        idx = []
        if len(self.distributions) == 0:
            for i in range(self.num_arms):
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
        self.arm_counts = np.zeros(self.env.num_arms)

        if value is not None:  # uniform initial values
            self.arm_values = np.array(
                [value for _ in range(self.env.num_arms)])
        else:  # it is None, then random values
            self.arm_values = np.random.normal(
                size=self.env.num_arms)

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
        for s in tqdm(range(steps),
                      desc='Agent running',
                      disable=~self.verbose):
            self.take_single_step()

            self.arm_counts[self.current_arm] += 1
            self.update_values()
            self.update_logs(s)

        self.simulation_finished = True
        return

    def describe(self):
        """Describe basic information about the agent's end state."""
        if not self.simulation_finished:
            tqdm.write('Agent has not run yet.')
        else:
            tqdm.write('\n======')
            tqdm.write('value history: ', self.values_history)
            tqdm.write('arm history: ', self.arms_history)
            tqdm.write('arm counts: ', self.arm_counts)
            tqdm.write('arm values: ', self.arm_values)


class GreedyAgent(Agent):
    """Greedy policy."""

    def __init__(self, env: TestBed, verbose: bool = False, **kwargs):
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


class Simulation:
    """Put an (new) agents in an (new) environment, run. Then repeat."""

    def __init__(
            self,
            env_type: TestBed,  # the Callable
            num_arms: int,  # number of arms
            agent_type: Agent,  # the Callable
            num_agents: int,
            init_value: int,
            step: int,
            random_seed: int = 42,
            **kwargs):
        """Combine the agent and the environment."""
        self.env_type = env_type
        self.num_arms = num_arms
        self.agent_type = agent_type
        self.num_agents = num_agents
        self.init_value = init_value
        self.step = step
        self.random_seed = random_seed

        self.agent_values_histories = []  # list of lists
        self.avg_values_history = None
        self.agent_arms_histories = []  # list of lists
        self.avg_arms_history = None

    def run_all_agents(self):
        """Run simulation."""
        for i in tqdm(range(self.num_agents), desc='Simulation running'):
            self.env = self.env_type(
                num_arms=self.num_arms,
                random_seed=self.random_seed + i)
            self.agent = self.agent_type(self.env)
            self.agent.init_values(self.init_value)
            self.agent.run(self.step)

            # collect results
            self.agent_values_histories.append(
                self.agent.values_history)
            self.agent_arms_histories.append(
                self.agent.arms_history)

    def aggregate_results(self, make_plot: bool = True):
        """Collect aggregated result from all the agent/env pairs."""
        self.avg_values_history = np.mean(
            self.agent_values_histories, axis=0)
        if make_plot:
            sns.set(font_scale=1.2)
            sns.set_style("whitegrid", {'grid.linestyle': '--'})
            sns.lineplot(x=range(len(self.avg_values_history)),
                         y=self.avg_values_history)
            plt.xlabel('Step')
            plt.ylabel('Average value')
            plt.title(f'Result from {self.num_agents} simulations.')
            plt.tight_layout()
            plt.show()



if __name__ == '__main__':

    simulation = Simulation(
        env_type=TestBed,
        num_arms=10,
        agent_type=GreedyAgent,
        num_agents=2,
        init_value=0,
        step=100)
    simulation.run_all_agents()
