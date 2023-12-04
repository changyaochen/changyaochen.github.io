---
layout: single
title:  "Large Language Model (LLM) learning notes, part 1"
date:   2023-12-05 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "blah more"
header:
  teaser: /assets/images/reinforcement-learning-fig.jpeg
---

Text generation before transformer: RNN.
RNN has a problem: long-term dependency, namely,
it can only remember the last few words, or it takes a long training time
if we want to remember words earlier in the sentence, as we need a bigger model.

Transformer is a new architecture that solves this problem.
It can be scaled efficiently to use multi-core GPUs, it can parallel process input data, making use of much larger training datasets, and crucially, it's able to learn to pay attention to the meaning of the words it's processing.

Transformer high-level overview.

In context learning: provide context to the model, so that it can learn the meaning of the words it's processing.

zero-shot learning

MLOps: size of the model.
