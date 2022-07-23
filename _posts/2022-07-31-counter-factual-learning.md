---
layout: single
title:  "Notes on Counterfactual Learning"
date:   2022-07-31 12:00:00 -0600
published: false
tag: [misc, machine learning]
toc: true
toc_sticky: true
excerpt: TODO
header:
  teaser: /assets/images/LP.png
---

# Agenda
What's the policy, how to connect with supervised learning and model?
How to connect with A/B test?

We want to choose a policy to maximize certain reward $$V(\pi)$$.

Role of data: they're observed rewards under the policy that is used.

A/B test can be considered as on-policy evaluation?

Off-policy evaluation (OPE): to estimate $$V(\pi_e) \approx \hat{V}(\pi_e, \mathcal{D}_0)$$
where $$\mathcal{D}_0$$ is data collected from policy $$\pi_0$$.

### Model-based OPE
"Model the world".

Traditional machine learning, train models to predict the counterfactual outcomes.
What's the problem? The data used from training might not coming from the same population where the trained policy is going to be applied.
As such, the model is biased.

### Model-free OPE (IPS)
$$\hat{V}_\text{IPS} = \frac{1}{n} \sum \frac{\pi_e(a_i | x_i)}{\pi_0(a_i | x_i)}r_i$$

This is unbiased.

### Practical use
What data to log? The 4-tuple: $$\mathcal{D}_0 = (x, a, r, p)_i$$, whereas the last is the propensity.
Here the policy used is $$\pi_0$$.

The hard problem: accurately predict the rewards, then the optimal policy falls out naturally, _e.g._, via $$argmin$$.
The easy problem: find the optimal policy, _i.e._, pick the correct action, whereas the reward prediction can be wrong.

The latter inspires the model-free approach. Empirical risk minimization.
