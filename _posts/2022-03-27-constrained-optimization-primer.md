---
layout: single
title:  "Notes on constrained optimization"
date:   2022-03-27 12:00:00 -0600
published: false
tag: [misc, machine learning]
toc: true
excerpt: A study note of constrained optimization, including linear simplex method, linear programming, and KKT conditions.
header:
  teaser: /assets/images/LP.png
---

Recently I came to learn the fantastic topic of constrained optimization, and here I want to summarize the study notes before it got lost in my pea-size brain. Also, I will gloss over any rigorous mathematical proofs, and only focus on the intuitions.

# A toy example
Optimization, in the very basic form and without loss of generality, is to find the minimum of an objective function \\(f(x)\\), over a space \\(x \in \mathbb{R}^n\\). Generally, we are interested in the global minimum, and as such, if we limit ourselves in the realm of convex optimization, then any local minimum is a global minimum. In addition, one can convert a maximization problem to a minimization problem by simply negate the objective function.