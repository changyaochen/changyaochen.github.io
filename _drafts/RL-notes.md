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
\pi(a|s):& ~~\text{The policy, the probability of taking action }a\\
         & ~~\text{, given the state }s.\\
q(\cdot):& ~~\text{The value function of }\cdot\text{, which can be }a\text{ or }s.\\
Q_t(\cdot): & ~~\text{The estimated value function, at time step }t.\\
\end{align}
$$

Action-values: the *expected* reward of taking an action.

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

END.
