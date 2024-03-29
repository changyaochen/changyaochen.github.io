---
layout: single
title:  "Notes on Reinforcement Learning"
date:   2023-01-01 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: TODO
header:
  teaser: /assets/images/wip.png
---

## MDP
How bandit and MDP are different: MDP considers the "long term impact" of the immediate actions, whereas bandit takes
action myopically. RL generally deals with MDP, and the goal is to maximize the future reward.

Policy defines that (deterministic or probabilistic) action under a given state.

Under a given policy, one can calculate the value function: it estimates the future return under this policy.
There are two types of value functions: action-value function, and state-value function.

$$
\begin{align}
v_{\pi}(s) &= \mathbb{E}_{\pi}[G_t | S_t = s]\\
q_{\pi}(s, a) &= \mathbb{E}_{\pi}[G_t | S_t = s, A_t = a]
\end{align}
$$

Bellman equation defines the relationship between the value of a state (or a state-action pair), and its possible successors.

$$
\begin{align}
v_{\pi}(s) &= \sum_{a} \pi(a | s) \sum_{s', r} p(s', r | s, a)\big[r + \gamma ~ \color{red}{v_{\pi}(s')}\big] \\
  &\text{for all } s \in \mathcal{S}\\
q_{\pi}(s, a) &= \sum_{s', r} p(s', r | s, a)\big[r + \gamma ~ \sum_{a'} \pi(a' | s') \color{red}{q_{\pi}(s', a')}\big]\\
  &\text{for all }s \in \mathcal{S}, a \in \mathcal{A}
\end{align}
$$

Bellman optimality equations are almost identical to the Bellman equations, expect replacing the "sum over all action $$a$$",
with "select the action that has the maximum value, _i.e._, $$\mathrm{max}_a$$.

## TODO
Calculate the value function of the random policy of the gridworld, figure 3.2 in the textbook.

To solve Bellmen equations analytically is not tractable, for large problems: there are just to many linear equations.

What is the optimal policy? Under the optimal policy, the value function at each state is largest among all possible policies.
How to find the optimal policy? For small problems (_e.g._, limited state and action space), one can find the optimal policy with brute force.

Bellmen equation: how to calculate the value function of a state. It can be solved, in principle, as it is set of linear equations.
Bellman optimality equation: it is under the optimal value functions and optimal policy.

From optimal value to optimal policy: just one-step look ahead and take $argmax$, that is:

$$
\pi_*(s) = \argmax_{a} \sum_{s', r}p(s', r \mid s, a)\big[r + \gamma v_*(s')\big]
$$

Policy evaluation and improvement

Policy evaluation (a.k.a, prediction) is the task to determine the state-value function, $v_\pi(s)$, for a given policy $\pi$.
This can be done by solving the Bellman equation,
which is a set of $|\mathcal{S}|$ linear equations, one for each state $s$.
What else need to be known? The transition probability $p(s', r \mid s, a)$ (a.k.a, the **model**),
and the discount factor $\gamma$.

However, in practice, one solve this problem iteratively, instead of using a linear system solver.

Policy improvement (a.k.a, control) is the task to improve the policy, that is, to find the policy, $\pi_*$, that maximize the value functions (rewards). Control is the ultimate goal of RL.

The policy improvement theorem: from the policy evaluation, one obtains the all the state-values. From, here, there is a way to achieve a equally good, or better policy, by taking greedy action at each state. Simply put, if the current policy $\pi$ instructs the action at the given state $s$, then a new policy $\pi'$ subscribes that $\pi'(s) = \argmax_a\sum_{s', r}p(s', r \mid s, a)[r + \gamma v_\pi(s')]$. Note the state-values are still under the current policy $\pi$.

Here we only discuss the deterministic policies.

There is a clear link between the policy evaluation (prediction) and policy improvement (control), and it is not hard to see the iterative nature. This is the so-called policy iteration algorithm, in order to find the **optimal** policy. Note that, a single policy evaluation step itself is also an iterative process, which only terminate after an exit condition is met, *i.e.*, the value-function stops changes between successive iterations.

Value iteration algorithm. The policy iteration algorithm evaluates the state-value functions for the *given* policy, that is, summing over $\pi(a\mids)$. Then it iteratively improves the policy by repeated policy evaluations. The value iteration algorithm side-step the policy evaluation step altogether: instead of finding the state-values for the given policy, it tries to find the *optimal* state-values directly. This is achieve by greedy selecting the action that maximize the state-value, *i.e.*, without following any policy.

<figure>
<center>
<a href="/assets/images/RL_policy_evaluation_control.png"><img style="width:75%;" src="/assets/images/RL_policy_evaluation_control.png"></a>
</center>
</figure>

Policy and value iteration algorithms are all based on Bellmen equations,
which is rooted in Dynamic Programming.
What are the other approaches?
* Monte Carlo method (sample based), for policy evaluation, *i.e.*, to find $v_\pi$. Also, here one does not need to know the model, $p(s', r \mid s, a)$.
* Brute-force method, for deterministic policy.


Monte-Carlo methods. In the DP paradigm, it requires us to know the transition probability, $$p(s', a \mid s, a)$$, this can be a tall task in reality.

DP is the means for policy evaluation, that is, for a given policy $$\pi$$, finding its state-value functions.

MC uses sample average as the estimate of the value functions (only applies to episodic case).

In the context of episodic tasks (with terminal states), with a given policy, after an episode is finished and collected the total rewards $$G$$, we can count from the back, and update the discounted rewards of the previous states. We can run through many episodes, so that we can collect multiple values of each state, and the state-value function can be estimated as the simple average. The same procedure can be used to estimate the action-value function.

How to ensure exploration in MC? Exploring starts: the initiate state, and more importantly, the initiate action is randomly chosen. In the following states, the agent will follow the prescribed policy.

How to use MC for control (_i.e._, policy improvement)? Simple, after each episode, when we are updating the state and action value functions, we can also update the policy by greedily select the action that has the largest action-value. Then for the next episode, we can follow the updated policy.

Limitation of exploring start? Maybe this is not feasible in reality. Taking a page from the $$\epsilon$$-greedy policy in the multi-armed bandit setting: when deciding which action to take, instead of deterministically follow the current policy, there is a small probability, _e.g._, $$\epsilon$$, the agent will choose a random action.

This will work for the control problem as well. In this way, we will have a stochastic policy, which might not be optimal, but we will bite the bullet.

## On-policy vs off-policy

On-policy: evaluates and improves the policy being used to select actions.
Off-policy: evaluates and improves a different policy from the ones used to select actions.

Target policy $$\pi(a \mid s)$$ vs behavior policy $$b(a \mid s)$$.

## Important sampling
This is how we do off-policy learning. In short, importance sampling uses samples from one probability distribution $$b(x)$$, to estimate the expectation of a different distribution $$\pi$$.

Simply put, we want to learn $$E_{\pi}[X]$$, however, we can only observe the outcome from following the behavior policy $$b$$. As a trick, we can expand the expectation under the target policy $$\pi$$ as:

$$
\begin{eqnarray}
E_{\pi}[X]
&= \sum_{x \in X} x \pi(x) \frac{b(x)}{b(x)} \\
&= \sum_{x \in X} x b(x) \frac{\pi(x)}{b(x)} \\
&\approx \frac{1}{N} \sum_i^N x_i \rho(x)
\end{eqnarray}
$$

## Off-policy prediction
Use the behavior policy to evaluate the target policy, _i.e._, what's the state-value functions.

