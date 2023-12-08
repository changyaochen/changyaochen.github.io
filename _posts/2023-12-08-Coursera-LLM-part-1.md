---
layout: single
title:  "Large Language Model (LLM) learning notes, part 1"
date:   2023-12-08 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "blah more"
header:
  teaser: /assets/images/reinforcement-learning-fig.jpeg
---
I have been putting off formerly learning about Large Language Models (LLMs)
for a while, with the excuse that I don't have time. Excuses are, at the end of
the day, excuses, so I try to do the easiest thing first: follow a Coursera
[course](https://www.coursera.org/learn/generative-ai-with-llms),
and try to take notes. This is the first part of my notes.

## Rise of LLMs: transformer architecture

LLMs, at the simplest level, are models to "finish sentences". To do so, we first
need to provide the "prompt" to the model, _i.e._, ask a question, so that the
model, which is so knowledgeable (since it is trained on massive amount of data),
can answer it.
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
