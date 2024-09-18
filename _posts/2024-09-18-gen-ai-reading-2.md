---
layout: single
title:  "Notes for Generative AI learning, part 2"
date:   2024-09-18 12:00:00 -0600
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

### Recurrent Neural Network (RNN)

RNN (Recurrent Neural Network) is a type of autoregressive model, that predicts the next element
in a sequence.
The elements of the sequence (_e.g._, words from a vocabulary, say, English) are usually represented
as embeddings (a vector of real numbers), that is, a one-to-one mapping such as
`"word" -> [0.1, 0.2, 0.3, ...]` (the key of the mapping is usually an integer, acting as the
index of the word in the vocabulary).

The characteristics of a RNN layer is the "hidden state", which carries a recurrent nature.
As the image below shows, to get a prediction from the RNN layer, one needs to feed it with
the sequence of $$[x_1, x_2, x_3, ...]$$ one by one, in order to get $$x_t$$ (a.k.a, $$y$$).
In this process, the hidden state $$h_{i-1}$$ from the previous step $$i$$ is combined with the input $$x_i$$,
to create, among other things, the new hidden state $$h_i$$.
This new hidden state will be used for the next iteration.

<figure>
<center>
<a href="/assets/images/rnn_schematic.png"><img src="/assets/images/rnn_schematic.png"></a>
<figcaption>
How does a RNN layer work. The input sequence is 200-long, and each element is a 100-dimensional
vector (embedding). The hidden state is 158-dimensional. The input element is encoded as a
100-dimensional vector. The hidden state is represented as a 158-dimensional vector.
</figcaption>
</center>
</figure>

Given the output of the RNN layer, how can we produce the desired output, which is an element
(_e.g._, an English word) from the vocabulary? The answer is to use a dense layer, whose
output size equals to the
size of the vocabulary. The dense layer will take the output of the RNN layer, and take the softmax
activation to produce the probability distribution whose support is the vocabulary. We can then
sample from this distribution to get the next word.

When training the RNN model, the loss function is usually the categorical cross-entropy loss,
which measures the difference between the predicted probability distribution and the true distribution.
Here the support of the distribution is the vocabulary.

### LSTM (Long Short-Term Memory)

The recurrent nature of RNN is designed for it to "remember" information
from previous elements. However, it is not very good at remembering
information from very far back: a naive approach would be including a longer
sequence of elements during the training process. In practice, this leads to the
vanishing/exploding gradient problem, where the network is incapable to learn
from the long-term dependencies.

The LSTM (Long Short-Term Memory) is a type of RNN that is designed to address this issue.
It modifies the RNN layer by adding a few "gates", each of which is responsible for
a dedicated task. For example, the "forget gate" is responsible for deciding whether to forget
(_i.e._, not to remember) information from the previous elements,
and the "input gate" is responsible for deciding
how much information to keep (_i.e._, not to forget) from the current element.

The figure below shows the schematic of the LSTM cell (copied from Chris Olah's
[blog](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)): aside from the
hidden state $$h$$, the LSTM cell also keeps (outputs) a cell state $$C$$
(the upper brach that flows through the cell). The values of both the hidden state
and the cell state are updated via a series of matrix multiplications and activation
(with either sigmoid, $$\sigma$$, or hyperbolic tangent, $$\tanh$$).

<figure>
<center>
<a href="/assets/images/lstm_schematic.png"><img src="/assets/images/lstm_schematic.png"></a>
<a href="/assets/images/lstm_annotation.png"><img src="/assets/images/lstm_annotation.png"></a>
<figcaption>
A concise schematic of the LSTM cell. The upper branch represents the cell state,
and the lower branch represents the hidden state.
</figcaption>
</center>
</figure>

A naive question (at least for me) is: why do we need both sigmoid and $$\tanh$$ activation,
_mathematically_, they can be combined with just one $$\tanh$$ function. The answer
stems from that, by separating the two activation functions, the LSTM cell can learn
more efficiently, as the two functions are responsible for different tasks.

### Gated Recurrent Unit (GRU)

The LSTM introduces a cell state to keep track of the long-term dependencies,
which inevitably increases the complexity of the model. The GRU (Gated Recurrent Unit)
is a simplified version in that it maintains just the hidden state, but makes
effort how the hidden state is updated, by taking a page from LSTM.
For example, it combines the forget and input gates into a single "update gate".

### PixelCNN: combining space and time

Previously, we have learned that we can use CNN (Convolutional Neural Network) to
incorporate the spatial information of the input data (_e.g._, images)
to learn the underlying patterns.

There isn't an apparent sequential nature with regard to the pixels in an image,
however, one could argue that, if we know enough "leading" pixels, we can predict
what the next pixel should be. Here we can define the ordering of the pixels
from top-left to bottom-right, row by row.

This is the intuition behind PixelCNN, which combines the sequential nature of
the autoregressive model to the spatial nature of CNN. The structure of PixelCNN
is quite similar to a CNN based autoencoder, only that we introduce a special "masked"
convolutional layer, where:

* The "second half" of the convolutional kernel is masked out, so that the
  convolutional layer can only "see" the pixels that have been processed.
* The center pixel of the kernel is either masked out, or not.

At generation time, we can feed the model with a partially filled image
(or a blank image), and let the model predict the next pixel, **based on the
preceding pixels**, so on and so forth, until the image is fully generated.

I personally find the PixelCNN model a bit less practically useful, as it
doesn't allow the user to provide meaningful input to the model,
such as a text prompt, or a latent vector (maybe not so meaningful...).
However, it is a good example
to show how one can combine different types of neural networks, in this case,
spatial and sequential, to learn the underlying patterns of the data.
