---
layout: single
title:  "Large Language Model (LLM) learning notes, part 3"
date:   2024-01-15 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "Learning notes from the Coursera course on Large Language Models (LLMs)"
header:
  teaser: assets/images/transformer_architecture.png
---

## Reinforcement Learning from Human Feedback (RLHF)

In a traditional supervised learning problem, the model prediction is either right or wrong.
In a language model, albeit falling under the definition of a supervised learning problem, it is
not so straightforward to define what is right or wrong. The model can generate a semantically
and logically correct sentence, but it might not be desireable, namely, aligned with
commonly perceived (moral) value. A prime example is that a language model can generate
toxic responses to a given prompt, or give instructions to make a bomb.



* LLM at heart is a supervised learning problem
* The predictions are probabilistic
* Alignment problem
* How to tune the model: not with the labels, but rewards

## LLM applications
RAG
