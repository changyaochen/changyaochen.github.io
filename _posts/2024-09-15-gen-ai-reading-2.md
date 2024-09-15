---
layout: single
title:  "Notes for Generative AI learning, part 2"
date:   2024-09-15 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "Scratch notes when reading the O'Reilly book of 'Generative Deep Learning, 2nd Edition'"
header:
  teaser: assets/images/oreilly_gen_ai_book.jpeg
---

## Chapter 5. Autoregressive Models

An autoregressive model takes the preceding elements of a sequence as input to predict the next element.
For example, a time-series model to predict the stock price for next day.
In the context of generative model, a typical application of autoregressive model
is in the generation of text, where the model predicts the next word in a sentence given the preceding words.

### LSTM model

LSTM (Long Short-Term Memory) is a type of RNN (Recurrent Neural Network) that can create
an autoregressive model.
The elements of the sequence (_e.g._, words from a vocabulary, say, English) are usually represented
as embeddings (a vector of real numbers), that is, a one-to-one mapping such as
`"word" -> [0.1, 0.2, 0.3, ...]` (the key of the mapping is usually an integer, acting as the
index of the word in the vocabulary).

The characteristics of an LSTM layer is the "hidden state", which carries the recurrent nature.
As the image below shows, to get a prediction from the LSTM layer, one needs to feed it with
the sequence of $$[x_1, x_2, x_3, ...]$$ one by one, in order to get $$x_t$$ (a.k.a, $$y$$).
In this process, the hidden state $$h_{i-1}$$ from the previous step $$i$$ is combined with the input $$x_i$$,
to create, among other things, the new hidden state $$h_i$$.
This new hidden state will be used for the next iteration.

<figure>
<center>
<a href="/assets/images/lstm_schematic.png"><img src="/assets/images/lstm_schematic.png"></a>
<figcaption>
How does an LSTM layer work. The input sequence is 200-long, and each element is a 100-dimensional
vector (embedding). The hidden state is 158-dimensional. The output is a 100-dimensional vector.
The output of the layer is a 158-dimensional vector, which is the hidden state of the last element.
</figcaption>
</center>
</figure>

Given the output of the LSTM layer, how can we produce the desired output, which is an element
(_e.g._, an English word) from the vocabulary? The answer is to use a dense layer, whose
output size equals to the
size of the vocabulary. The dense layer will take the output of the LSTM layer, and take the softmax
activation to produce the probability distribution whose support is the vocabulary. We can then
sample from this distribution to get the next word.

When training the LSTM model, the loss function is usually the categorical cross-entropy loss,
which measures the difference between the predicted probability distribution and the true distribution.
Here the support of the distribution is the vocabulary.

The details of the LSTM layer is a bit complicated (or convoluted), but by now they are mostly
abstracted away by the deep learning libraries, such as TensorFlow or PyTorch.

