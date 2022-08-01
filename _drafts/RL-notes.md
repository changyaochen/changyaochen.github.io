---
layout: single
title:  "Notes on Reinforcement Learning"
date:   2022-08-31 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: TODO
header:
  teaser: /assets/images/wip.png
---

Reinforcement learning (RL) is about decision making, _i.e._, learn a policy.
The decision maker (the agent) generates the training data by interacting with the world.
This is in contrast to the supervised learning where there are already label provided.
In RL, the agent must learn the consequence (label) from its own actions through trial and error.

## Nomenclature
Common naming conventions in the RL context.
We commonly use the subscript $$t$$ to denote the time step.

$$
\begin{align}
a:& ~~\text{An action, for example, turn left, turn right.}\\
\mathcal{A}:& ~~\text{The set of all possible actions.}\\
A_t:& ~~\text{The specific action taken at time step }t.\\
r:& ~~\text{Reward of taking a certain action.} \\
  & ~~\text{Therefore, it is often expressed as } r|a.\\
R_t:& ~~\text{The reward observed at time step }t.\\
s:& ~~\text{A given state of the environment.}\\
\mathcal{S}:& ~~\text{The set of all possible states.}\\
S_t:& ~~\text{The state at time step }t.\\
\pi(a|s):& ~~\text{The policy, the probability of taking action }a,\\
         & ~~\text{given the state }s.\\
v(s):& ~~ \text{The value function of a state } s.\\
q(s, a):& ~~\text{The action-value function of }s, a.\\
Q_t(s, a):& ~~\text{The estimated action-value function, at time step }t.\\
p(s', r | s, a):& ~~\text{The joint probability distribution of transition.}
\end{align}
$$

Action-values: the *expected* reward of taking an action.

Policy: It is a mapping from a given state, $$s$$, to the probability of taking action $$a$$.
The notion of $$|$$ in the $$\pi$$, it is to emphasize it is a conditional probability distribution.

$$
\begin{align}
q_*(a)
:=&~\mathbb{E}[R_t | A_t = a]\\
=&~\sum_r r \cdot p(r|a)
\end{align}
$$

>If the action-values are known, the problem is solved.

The goal of the agent is to choose the action $$a$$ that has the largest action-value.
To do so, the agent wants to get $$q_*(a)$$ as accurately as possible.
One approach is the sample-average. With more observations, one needs to update the estimated action-values.
A general update rule is to update it incrementally. It works in the sample-average case, but also in non-stationary case.

Usually, one can observe the reward immediately, as $$R_t$$, then one can update the action-value estimation as:

$$
Q_{t+1} = Q_t + \alpha_t (R_t - Q_t)
$$

There is a question about what the initial value, $$Q_0$$, to use. The optimistic initial values approach assigns a large
value of $$Q_0$$, to encourage exploration early on. But it doesn't allow for continuous exploration later, for example,
to account for non-stationary rewards.

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

From optimal value to optimal policy: just one-step look ahead and take $argmax$

END.
