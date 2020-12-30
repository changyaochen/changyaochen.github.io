---
layout: single
title:  "Machine Learning Design Patterns: Model Training"
date:   2020-12-30 12:00:00 -0600
published: false
tag: [book, machine learning]
toc: true
excerpt: Here we look into a good resource of practicing good machine learning design patterns.
header:
  teaser: /assets/images/mldp.jpeg
---
In Useful Overfitting, we forgo the use of a validation or testing dataset because we want to intentionally overfit on the training dataset. In Checkpoints, we store the full state of the model periodically, so that we have access to partially trained models. When we use checkpoints, we usually also use virtual epochs, wherein we decide to carry out the inner loop of the fit() function, not on the full training dataset but on a fixed number of training examples. In Transfer Learning, we take part of a previously trained model, freeze the weights, and incorporate these nontrainable layers into a new model that solves the same problem, but on a smaller dataset. In Distribution Strategy, the training loop is carried out at scale over multiple workers, often with caching, hardware acceleration, and parallelization. Finally, in Hyperparameter Tuning, the training loop is itself inserted into an optimization method to find the optimal set of model hyperparameters.

In [continuing reading]({{ site.baseurl }}{% link _posts/2020-12-27-ML-design-pattern-1.md %}) the [Machine Learning Design Patterns](https://learning.oreilly.com/library/view/machine-learning-design/9781098115777/) book, in this post, I would like to summarize the takeaways from the Model Training section (Chapter 4). Most of the discussion are based on the neural network (NN) cases.

## Useful Overfitting

In almost all cases, overfitting is a bad thing, since we usually building models with the presence of noise. Overfitting usually means we are learning the noise which is inherently random. However, there are noise-free use cases, such as using an ML model to solve non-tractable deterministic problems (*e.g.*, partial differential equations, chaotic systems), that overfitting is actually the desired behavior.

Aside from the above, less-common, situation, (intentional) overfitting can useful in the general-purpose ML problems. When working on a new problem, one can (and should) intentionally overfit the model on a small subset of the data (*e.g.*, one batch), to ensure the model is sophisticated enough to handle the full data volume. This seems to be a good practice that comes with no cost.

## Checkpoints

This design pattern suggests to save the full model states periodically during the model training process. Here we have two questions need to answer: what do we mean by full model states, and how often is considered appropriate for "periodically".

### Full model states v.s. model artifact
When we say model artifact, it is referred to the information needed to make inference, such as the NN architecture and weights. On the other hand, the full model states, will not only include the model artifact, but also information needed to perform next iteration of the model training. The difference becomes crystal clear if one encounters hardware failure during training, which is not uncommon for NN models taking hours or days to train. Having merely the model artifact will not allow one to resume training, as we also need to know what is the current batch/epoch, learning rate (if we are following learning rate schedule). For recurrent NN, we might also need to know history of previous input values.

### Batch, virtual epoch, epoch
Let's save the full model states (checkpoints) as often as possible then! The atomic unit in NN model training is a batch, so why not export the model state after each batch? The problem is that such frequent snapshot will bring heavy disk I/O overhead, and increase the total training time. For example, if we have 16 million samples, and with batch size of 32, there will be half million checkpoints for just one epoch!

The next natural choice is to export the model state after each epoch. Although logically, it might not be optimal when dealing with large dataset. For such cases, one could probably only go through the full dataset a few iterations (epochs), and the resulting sparse checkpoints would not serve its purpose well.

The trade-off is what is called virtual epoch. In such situation, one specifies: 1) total number of iterations over a single sample (can be non-integer), 2) total number of checkpoints, 3) batch size. With that, we can calculate the total **number of steps (virtual epochs)** for the full training, and each virtual epoch will contain multiple batches. We will save checkpoints after each virtual epoch, such as:

~~~py
NUM_TRAINING_EXAMPLES = 1000 * 1000
STOP_POINT = 14.3
TOTAL_TRAINING_EXAMPLES = int(STOP_POINT * NUM_TRAINING_EXAMPLES)
BATCH_SIZE = 128
NUM_CHECKPOINTS = 32
steps_per_epoch = (
  TOTAL_TRAINING_EXAMPLES // (BATCH_SIZE * NUM_CHECKPOINTS)
)
~~~

### How checkpoints can help
Aside from the benefit describe above,

Retraining, warm start
<figure>
<center>
<a href="/assets/images/mldp_0411.png"><img src="/assets/images/mldp_0411.png"></a>
</center>
</figure>

Training batch, step, epoch.

## Transfer Learning
Mostly used in the context of image of text domains, where you can apply a similar task to the same data domain, but not so much for tabular data, as there are potentially infinite number of possible prediction tasks and data types.

## Distribution Strategy

synchronous versus asynchronous

Data parallelism versus model parallelism

Minimize I/O bottleneck
<figure>
<center>
<a href="/assets/images/mldp_0422.png"><img src="/assets/images/mldp_0422.png"></a>
</center>
</figure>

## Hyperparameter Tuning

grid search and combinatorial explosion
Bayesian optimization is a technique for optimizing black-box functions. Bayesian optimization defines a new function that emulates our model but is much cheaper to run. This is referred to as the surrogate function—the inputs to this function are your hyperparameter values and the output is your optimization metric.

I found [this video](https://www.youtube.com/watch?v=c4KKvyWW_Xk) a good introduction to Bayesian optimization (and the [corresponding tutorial](https://arxiv.org/pdf/1807.02811.pdf)),


