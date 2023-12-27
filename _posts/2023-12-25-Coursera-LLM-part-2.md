---
layout: single
title:  "Large Language Model (LLM) learning notes, part 2"
date:   2023-12-25 12:00:00 -0600
published: true
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "Learning notes from the Coursera course on Large Language Models (LLMs)"
header:
  teaser: assets/images/transformer_architecture.png
---
LLM, at the simplest level, is a model to "finish the sentences".
The model is trained as a supervised learning problem, where the training data
consists of inputs as the "unfinished" sentences, and labels as the next token
in the "finished" sentences. For example, a training sample can be:

> Input: "Sir Issac Newton developed"<br>
> Label: "calculus"<br><br>
> Input: "Sir Issac Newton developed calculus and the law of"<br>
> Label: "motion"

Note that, the start and end of the sentence are special tokens. As such,
any prediction can be compared with the "ground truth" label to generate
some kind of error metric, which can be used to evaluate the model.

## Evaluation metrics
In LLM, the evaluation metrics depend on the task at hand.

### ROUGE
Recall-Oriented Understudy for Gisting Evaluation, or
[ROUGE](https://en.wikipedia.org/wiki/ROUGE_(metric)),
 is the metric used in summarization tasks. It measures the token-level
"overlap" between the model prediction and the ground truth. Here we need to
pay attention to the "token-level", as it can be uni-gram, bi-gram, or even n-gram.
The difference is what's the atomic unit of comparison. For example, for uni-gram,
the atomic unit is a single token (_e.g._, "this"), and for bi-gram, the atomic unit
is two consecutive tokens (_e.g._, "this is").
Correspondingly, the ROUGE metric can be ROUGE-1, ROUGE-2, ROUGE-N, etc.

For example, if the ground truth is

><span style="color:green">"this is a test"</span>

and the model prediction is

><span style="color:blue">"that too is a test"</span>

then the ROUGE-1 recall is 3/4, the ROUGE-1 precision is 3/5,
and the ROUGE-1 F1 score is the 2/3 (the harmonic mean of recall and precision).
For ROUGE-2, the atomic unit will be bi-gram, and the ROUGE-2 recall is 2/3, as
the matching units are "is a" and "a test". We can compute the ROUGE-2 precision and
ROUGE-2 F1 score similarly.

There is, however, a special type of ROUGE metric called ROUGE-L. In this case,
we care about the longest common subsequence (LCS) between the model prediction
and the ground truth. For example, with the above example, the LCS is "is a test",
therefore the ROUGE-L recall is 3/4, the ROUGE-L precision is 3/5, and the ROUGE-L
F1 score is 2/3.

Note that, oftentimes, the recall metric is used as the default ROUGE metric.

### BLEU
Bilingual Evaluation Understudy, or [BLEU](https://en.wikipedia.org/wiki/BLEU)
is the metric used in machine translation tasks. It is closely related to ROUGE precision,
as it can be thought of  as the [geometric mean](https://en.wikipedia.org/wiki/Geometric_mean)
of ROUGE precisions with different lengths.

BLEU will be a value between 0 and 1, where 1 means the model prediction is identical
to the ground truth, and 0 means the model prediction is completely different from the
ground truth.

## Parameter Efficient Fine-Tuning (PEFT)
Now we have established the evaluation metrics, we can talk about model training.
As noted in the previous post, LLM model training is a very expensive process, therefore,
one usually leverages pre-trained models to fine-tune it on the task at hand. That
is, we take the parameter values from the pre-trained model, and use them as the initial
values to continue gradient descent on the task-specific data.

However, such fine-tuning still modifies **all** the model parameters, which for
large models, runs in the range of 10s or 100s billions. This can still be a
computationally expensive process. To address this issue, we can use a technique
called Parameter Efficient Fine-Tuning (PEFT).

### LoRA
One of the PEFT approaches is  Low rank adaption, or [LoRA](https://arxiv.org/abs/2106.09685).
The idea is very simple: in the pre-trained LLM, there are multiple matrices, such as the query
matrix. We will not touch those matrices, but instead, we will add a new matrix to each (or
only some) of them, and use the summed matrices when making inference. For these new matrices,
they are the outer product of two smaller matrices.

For example, if the original matrix is $$W_0 \in \mathbb{R}^{d \times k}$$, then the
injected matrix $$\Delta W_0$$ will have the same shape, but it can be decomposed as
$$\Delta W_0 = B A$$, where $$B \in \mathbb{R}^{d \times r}$$ and
$$A \in \mathbb{R}^{r \times k}$$. Here $$r$$ is much smaller (order of magnitude)
than either $$d$$ or $$k$$. In this way, the number of trainable parameters are
reduced from $$d \times k$$ to $$r \times(d + k)$$.

### Soft prompt tuning
In the previous post we talked about prompt engineering, which can be viewed as
a trial-and-error process, and the prompts are also in the form of human-readable text.
For soft prompt tuning, we move the "prompt" into the model, for example, as a 10-token
sequence that prefixes the input. During the fine-tuning process, we will only learn the
embedding of the prompt tokens using the task-specific data. In this way, the total
number of trainable parameters is much smaller than the original model, as we will
only train the embedding of the prompt tokens.
