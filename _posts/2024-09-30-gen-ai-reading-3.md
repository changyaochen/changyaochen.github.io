---
layout: single
title:  "Notes for Generative AI learning, part 3"
date:   2024-09-30 12:00:00 -0600
published: false
tag: [machine learning, book]
toc: true
toc_sticky: true
excerpt: This post is for chapter 6 (Energy-based models) and chapter 7 (Diffusion models).
header:
  teaser: assets/images/oreilly_gen_ai_book.jpeg
---

I found the organization of the chapter 6 is less intuitive, so I did
a bit of my own reading and think the energy-based models is closed related
to the diffusion models (chapter 7). I will combine these two chapters in this post.

My understandings are mostly from [this](https://yang-song.net/blog/2021/score/) blog.

We want to learn $$p(x)$$, and the obvious approach is the maximum likelihood estimation (MLE),
where given a candidate model $$p(x; \theta)$$, we learn the parameters $$\theta$$ by maximizing
the log likelihood of the training data $$\Sigma_i \log p(x_i; \theta)$$.

We can learn an arbitrary function $$f(x; \theta)$$ to approximate the true distribution $$p(x)$$,
but the issue is that: first $$f(x; \theta)$$ is not guaranteed to be positive,
and second, it is not guaranteed to satisfy the probability distribution
function constraint of $$\int_y f(y; \theta) = 1$$.
To address them,
we can transform and normalize the score function as:

\begin{equation}
p(x; \theta) = \frac{e^{-f(x; \theta)}}{Z(\theta)}, \tag{1}
\label{eq:probability_definition}
\end{equation}

where $$Z(\theta) = \int_y p(y; \theta) \textbf{d}y$$ is a
normalization constant to ensure the distribution is valid.

VAE and GAN bypass this by enforcing the latent variable follows a Gaussian distribution
to start with; normalizing flow models bypass this by starting from a latent Gaussian distribution and applying a series of invertible transformations to the latent variable.

## Energy-based models

We can draw an analogy between equation ($$\ref{eq:probability_definition}$$)
and [Boltzmann distribution](https://en.wikipedia.org/wiki/Boltzmann_distribution)
in statistical physics, which prescribes the probability of a system being in a certain energy state. The higher the energy, the smaller the probability.

Contrastive Divergence (CD) is a popular method to train energy-based models.

## Learning the gradient of the distribution

Instead of directly learning the distribution of $$p(x)$$ (via MLE),
we can learn the **gradient** of the (log-) distribution
to maximize the likelihood. Note here the gradient is with respect to the
input $$x$$, not the parameters $$\theta$$. This gradient is also called the
**score function**, namely, $$s_\theta(x) = \nabla_x \log p(x; \theta)$$.


