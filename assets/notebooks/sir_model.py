"""SIR model simulations."""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
from typing import Union, Dict, List


class SIR:
    """Vanilla SIR model."""

    def __init__(
            self,
            param: Dict = {}):
        """Only initialize the model parameters."""
        self.beta = param.get('beta', 0.1)
        self.gamma = param.get('gamma', 0.05)
        self.p_d = param.get('p_d', 0.01)
        self.X_init = None
        self.X = None
        self.num_steps = 0

    def run(
            self,
            X_init: Union[List, np.ndarray],
            num_steps: int = 365):
        """Run the simulation by solving the SIR ODE numerically."""
        self.X_init = X_init
        self.num_steps = num_steps

        # we want to simulate S, I and R, plus D (death)
        m = 4
        assert(len(X_init) == m)

        # initialize the X array
        self.X = np.zeros(shape=(m, self.num_steps))
        for i in range(m):
            self.X[i][0] = self.X_init[i]

        # solving the ODE
        for t in tqdm(range(1, self.num_steps)):
            S, I, R, D = self.X[0][t - 1], self.X[1][t - 1], \
                self.X[2][t - 1], self.X[3][t - 1]
            dS = -1. * self.beta * S * I / (S + I + R)
            dI = -1. * dS - self.gamma * I
            dR = (1 - self.p_d) * self.gamma * I
            dD = self.p_d * self.gamma * I

            self.X[0][t] = S + dS  # update S
            self.X[1][t] = I + dI  # update I
            self.X[2][t] = R + dR  # update R
            self.X[3][t] = D + dD  # update D

    def make_plot(self):
        """Visualize the simulation results."""
        if self.X is None:
            tqdm.write('Run the simulation first.')
            return
        sns.set(font_scale=1.2)
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        # _ = plt.figure(figsize=(12, 9))

        time_steps = list(range(self.num_steps))

        sns.lineplot(x=time_steps, y=100 * self.X[0, :], label='Susceptible')
        sns.lineplot(x=time_steps, y=100 * self.X[1, :], label='Infectious')
        sns.lineplot(x=time_steps, y=100 * self.X[2, :], label='Recovered')
        sns.lineplot(x=time_steps, y=100 * self.X[3, :], label='Death')

        plt.xlabel('Day')
        plt.ylabel('Proportion of population (%)')
        plt.legend()
        plt.show()
