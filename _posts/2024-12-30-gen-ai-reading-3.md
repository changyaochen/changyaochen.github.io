---
layout: single
title:  "Notes for Generative AI learning, part 3"
date:   2024-12-30 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: How the transformer architecture works.
header:
  teaser: assets/images/oreilly_gen_ai_book.jpeg
---
(I am having a hard time grasping the energy-based model and the related diffusion models,
therefore I will skip this part for now.)

## Chapter 9: Transformers

The most important architecture in the recent years is without a doubt the transformer.
It originates in the Natural Language Processing (NLP) field, and has been applied to
other fields, notably, in sequential modeling. This includes autoregressive models
(predicts the next token in a sequence, think chatGPT), and also sequence-to-sequence
models (translation between languages).

The vanilla transformer (namely, the original 2017 paper) discusses an autoregressive
fashion. The improvement of the transformer over the previous state-of-the-art
(Recurrent Neural Networks, RNNs) is the ability to parallelize the computation.
In RNN, each token in the sequence is processed sequentially, and the latent information
from the last token in sequence is used for inference (_e.g._, predict the next token).
This requires all the relevant information is encoded the last hidden state, therefore
greatly limits how well a RNN can "pay attention" to the information from the earlier portion
of the sequence.

The transformer architecture essentially exposes all the hidden states from all the tokens
in the sequence, and set up a mechanism, for different task ("query"), to "pay attention"
to different previous tokens ("key") with different degrees of relevance ("value").

Take the following example: we want to predict the next word after
"the pink elephant tries to get into the car but it was too ___". We, as human, would think a
proper word for the blank is "big", not because we have seen "pink" in the sentence, but because
we have seen "elephant" and "car" in the sentence (plus our knowledge of the world).
Under the transformer setting, the query is the word "too" (as we are asking for the next word
after it), and the keys are all the words in the sentence. We want to find the "relevance"
between the query and the keys, and in mathematical terms, we can express them as product between
the query vector and the key vectors (_i.e._, a matrix). The resulting vector prescribes how much
attention (_i.e._, weight) the query should pay to each key.

We can then apply the attention weights to the values. The value for each token can be thought as
the **un**weighted contribution. By multiplying the attention weights to the values, we get the
so-called contextualized value (vector), which is used to make the prediction.

<figure>
<center>
<a href="/assets/images/transformer_attention_head.png"><img src="/assets/images/transformer_attention_head.png"></a>
<figcaption>
How does the query, key, and value work in the attention head. Note that the dimensions for
the key and the value does not have to be the same, but the query and the key must have the
same dimension.
</figcaption>
</center>
</figure>

What described above constitutes a single attention head. The transformer architecture
consists of multiple attention heads, and the output from each attention head is then
concatenated and pass through a few other layers, such as residual connection,
layer normalization, and fully connected layers. These components have less to do with
the attention mechanism, but mostly needed to the neural network to train.
