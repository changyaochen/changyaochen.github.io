---
layout: single
title:  "Large Language Model (LLM) learning notes, part 1"
date:   2023-12-08 12:00:00 -0600
published: true
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "Learning notes from the Coursera course on Large Language Models (LLMs)"
header:
  teaser: assets/images/transformer_architecture.png
---
I have been putting off formally learning about Large Language Models (LLMs)
for a while, with the excuse that I don't have time. Excuses are, at the end of
the day, excuses, so I try to do the easiest thing first: follow a Coursera
[course](https://www.coursera.org/learn/generative-ai-with-llms),
and try to take notes. This is the first part of my notes.

## Rise of LLMs: transformer architecture

LLMs, at the simplest level, are models to "finish sentences". To do so, we first
need to provide the "prompt" to the model, _i.e._, ask a question, so that the
model, which is so knowledgeable (since it is trained on a massive amount of data),
can answer it. Here the emphasis is on the **"massive amount of data"** part.

Before circa 2017, the state-of-art model for text generation is Recurrent Neural
Network (RNN), with variants such as Long Short-Term Memory (LSTM) and Gated
Recurrent Unit (GRU). While successful, RNN has a crucial problem, that is it can
not handle long-term dependency very well. Namely, it can only practically remember
the last few words. If we want the model to remember earlier words, we need to
expand the size of model rapidly, to the point it can not be trained efficiently.

Then came the seminal paper, [Attention Is All You Need](https://arxiv.org/abs/1706.03762),
which proposed the transformer architecture that solves this problem.
We will probably have a separate post on the transformer architecture, but for now,
all we need to know is that this architecture breaks the sequential nature in the RNN
training routine, so that it can be scaled efficiently to use multi-core GPUs.
This allows transformer models to process training data in parallel, making use of
much larger datasets. More crucially, it's able to learn to pay attention
to the meaning of the words it's processing.

## Prompt engineering
At inference time, we, as the end user, provide the prompt to the model, so that
it can complete the sentence(s) for us. As the saying goes, "to get a good answer,
you need to ask a good question". The same apply to LLMs: there are techniques to
how to strut the prompt (question), so that the model can give us the best answer.

In the setting of LLMs, this is called prompt engineering. One of such techniques
is "in context learning": we can provide our context to the model, and since LLMs
are good at remembering things, they can use the context to give us a better answer.

To make in context learning more concrete, there is so-called _zero-shot learning_.
In this setting, we provide the **exact** structure of the desired conversation,
such as:

> Question: What is the meaning of life?<br>
> Answer:

Here we effectively leave the blank for the model to fill in, and hope that the
model will give us the answer: 42.

However, giving the model just the structure of the conversation is not enough
to produce the desired answer. In addition, we need to provide one or more examples,
and this is called _one-/few-shot learning_. For example, we can provide the following
prompt:

> Question: what is the sentiment of this review: this movie is great!<br>
> Answer: positive.<br>
> Question: what is the sentiment of this review: this movie is terrible!<br>
> Answer:

By showing the model "how it should be done", will increase the chance that you
will get the desired outcome.

## Temperature setting
A distinct feature of LLMs is that they are _probabilistic_ models. This means
with the same prompt (input), the model can give you different answers (output).
The level of such randomness can be controlled by the so-called _temperature_
parameter.

As LLMs predict the next token (word) one-by-one (based on the previous
tokens), on each instance, it gives the probability of each token in the vocabulary.
To pick the next token, one can simply pick the token with the highest probability
(greedy), or sample the vocabulary based on the probability of each token. It is
the latter approach that gives us the randomness.

Oftentimes, we apply a softmax function to the probability distribution, before
we draw the next token, and the temperature parameter $T$ is inserted into the softmax.
For example, if the probability distribution for the next token is $$p(w_i)$$, then
the probability of drawing the token $w_i$ is:

$$
\frac{\exp(\frac{p(w_i)}{T})}{\sum_{j}\exp(\frac{p(w_j)}{T})}
$$

As you can see, if $$T=1$$, then we have the exact softmax function. If $$T$$ is
close to 0, then we are getting closer to the greedy scenario: the token $$w_i$$ with the
highest probability $$p(w_i)$$ will almost always be picked. On the other hand,
if $$T$$ is very large, we are getting closer to the uniform distribution: all tokens have the same probability of being picked.
## MLOps
Finally, let's get practical: how much computation resource is required to deploy,
or even to train an LLM? We can start with some back-of-the-envelope calculation.
Let's say the LLM has 1 billion parameters. If we use 32-bit (4-byte)
floating point to represent each parameter, then we need 4GB of memory to
store/deploy the model. However, it is very common for LLM to have more than 100
billion parameters, so we are talking about 400GB of memory, probably don't try this
at home.

For model training, not only we need to store the model parameters in memory,
and we also need to store the gradients, and a lot other things (optimizer states,
etc.). As a rule of thumb, we might need **20x** of the model size to train the model.

## Scaling laws
Do we really need 100 billion parameters to train a good LLM? How about using
a smaller model (fewer parameters), but with more training data? It is conceivable
that with a fixed computation budget, to achieve the same level of model performance,
there might be trade-off between model size and training data size. This is where
the [Chinchilla scaling law](https://en.wikipedia.org/wiki/Neural_scaling_law#Chinchilla_scaling_(Hoffmann,_et_al,_2022))
comes in. It states that:

> the optimal training data size (number of tokens)
> **20x** of the model size (number of parameters), and vice versa.

So spend your computational budget wisely!
