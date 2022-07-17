---
layout: single
title:  "Notes on optimization: the basics"
date:   2022-03-27 12:00:00 -0600
published: true
tag: [misc, machine learning]
toc: true
excerpt: A series of study notes of optimization, including convex optimization, linear programming, linear simplex method, and KKT conditions.
header:
  teaser: /assets/images/LP.png
---

Recently I came to learn the fantastic topic of constrained optimization, and here I want to summarize the study notes before they got lost in my pea-sized brain. Also, I will gloss over any rigorous mathematical proofs, and only focus on the intuitions.

## A toy example
Optimization, in the very basic form and without loss of generality, is to find the minimum of an objective function \\(f(x)\\), over a space \\(x \in \mathbb{R}^n\\). Generally, we are interested in the global minimum, and as such, if we limit ourselves in the realm of convex optimization, then any local minimum is a global minimum. In addition, one can convert a maximization problem to a minimization problem by simply negating the objective function.

Arguably the simplest example is to minimize the function \\( f(x) = x^2 \\) for \\(x \in \mathbb{R}\\). The solution is \\(x^\ast = 0\\) with \\( f(x^\ast) = 0 \\). One simply solves for the first order condition of \\(\nabla f(x) = \textbf{d}f(x) / \textbf{d}x = 2x = 0 \\).

It is also clear that one can not find the minimum for \\( g(x) = x^3 \\) over the same \\(\mathbb{R}\\) domain, despite one can seemingly solve for the first order condition of \\(\nabla g(x) = 0\\) too.

## Convex optimization
The reason that we can solve the optimization problem for the above quadratic function, but not for cubic function, both of which are over the \\(\mathbb{R}\\) domain, is that the former is a convex optimization and the latter is not.

The more formal definition of  convex optimization is that, we try to minimize a **convex function** over a **convex set**.

### Convex function and convex set
The questions beg for answers are then: what is a convex function, and a convex set?

Formally, a function \\(f(x)\\) is convex, if for all \\(0 \lt \lambda \lt 1\\), we have \\(f(x + (1 - \lambda)y) \le \lambda f(x) + (1 - \lambda)f(y)\\). Some example of convex functions are \\( x, x^2, \|x\|, e^x \\). For a given function, one can prove its convexity using the definition, but more often than not, one proves via other properties that are tied to the convexity. The most commonly used approach is through the second order condition, which states that a function \\( f(x) \\) is convex, if and only if its Hessian \\( \nabla^2 f(x) \\), if exists, is non-negative. Here we used the term Hessian, since \\( \nabla^2 f(x) \\) could very well be a matrix. For a matrix to be "non-negative", it means it is [positive-semidefinite](https://en.wikipedia.org/wiki/Definite_matrix). Therefore, the burden of the proof shifts to demonstrating a matrix if positive-semidefinite. In this regard, a convenient route is that, a matrix \\(M\\) is positive semi-definite if and only if all of its eigenvalues are non-negative.

Similarly, a set \\(\Omega\\) is convex, if for all \\(0 \lt \lambda \lt 1\\), and \\(x \in \Omega, y\in \Omega\\), we have \\(\lambda x + (1 - \lambda)y \in \Omega\\). For example, the real number is a convex set, and so is a [Euclidean ball](https://en.wikipedia.org/wiki/Ball_(mathematics)).

A note on convex or strict convex: the latter corresponds to the case where the inequality conditions are strictly satisfied.

### Why obsess with convexity
If we are dealing with a convex optimization problem, then any local minimum is a global minimum. As such, the **necessary conditions** for a local minimum can be derived from the first order condition, namely, the gradient \\( \nabla f(x) \\) equals to zero. Note that in absence of convexity (the function is not convex), this first order condition is not even a sufficient condition for local minimum (think \\(f(x) = x^3 \\)).

A side note: for a local minimum, other than the first order condition \\( \nabla f(x^\ast) = 0 \\), another necessary condition is about the second order condition of \\( \nabla^2 f(x^\ast) \succcurlyeq 0 \\). A convex function automatically satisfies this requirement. In essence, the following three statements are identical (we assume both \\(x, y\\)) are feasible:
* \\(f(x)\\) is convex.
* \\(f(y) \ge f(x) + \\nabla f^T(x) (y - x)\\).
* \\( \nabla^2 f(x) \succcurlyeq 0 \\).



## Linear regression as convex optimization
In linear regression, the objective function (to minimize) is the sum of squared error \\(\mathcal{L(\beta)}\\), as:

$$
\mathcal{L}(\beta) = (y - X\beta)^T (y - X\beta).
$$

It turns out, this is a convex optimization problem, as the Hessian matrix \\(\\nabla^2 \mathcal{L} = 2 X^T X\\) is positive-definite. This can be proved directly from the definition of positive-definite, that is, for any given vector \\(v\\), the value of \\(v^T (X^T X) v = \|\|Xv\|\|_2^2 \ge 0\\), and the equality is only binding for \\(v = 0\\). As such, the local minimum is the strict global minimum, and the solution of the local minimum can be obtained by solving the first order condition (that is, the normal equation), through:

$$
\beta^\ast = (X^T X)^{-1} X^Ty.
$$

This is the reason why we can safely use this convenient solution in linear regression (or gradient descent for the matter). Similarly, the objective function in logistic regression (cross-entropy) is also convex, despite without a close-form solution.

## Takeaways

Here we are just going through some basic concepts of optimization, and place special attention of the sub-field of convex optimization.

* A convex optimization problem is where the objective function is convex, over a domain that is a convex set. Note that a linear function is always convex (relevant to Linear Programming).
* In general, checking convexity can be a very difficult problem, and we often rely on the characterizations of convex functions that make the task of checking convexity somewhat easier.
* The first order condition (\\(\nabla f(x) = 0\\)) is a **necessary** condition for local optimality (think \\(f(x) = x^3\\)). Only for convex optimization problems, this becomes a **sufficient** condition as well.
