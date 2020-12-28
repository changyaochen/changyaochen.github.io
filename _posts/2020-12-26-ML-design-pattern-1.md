---
layout: single
title:  "Machine Learning Design Patterns: Reproducibility"
date:   2020-12-28 12:00:00 -0600
published: false
tag: [book, machine learning]
toc: true
excerpt: blah
header:
  teaser: /assets/images/mldp.jpeg
---
It has been a few busy months since I started at Instacart, and finally I can catch some breath during the holiday break. Ruling out the possibility of travel, it allows for more time to read a few books. To this end, I've been plowing through this wonderfully book: [Machine Learning Design Patterns](https://learning.oreilly.com/library/view/machine-learning-design/9781098115777/) by Valliappa Lakshmanan, Sara Robinson, and Michael Munn. The book is relatively recent, and largely based on (but not necessary bounded by) Google BigQuery and tensorflow/keras frameworks. One thing I truly appreciate about this book is that, it is organized as independent modules, such that for a reasonably adept machine learning (ML) practitioner, one can easily pick up the area of interests and dive in.

I strongly resonate with many of its content, and reckon it would be a good idea to summarize the key points, to the very least, for my own future reference. In this post, I will focus on the **Reproducibility Design Patterns** (Chapter 6 of the book).

## Transform
The key idea of this pattern is to separate *input*, *feature*, and *estimator*. As a whole, they consist of what is considered a *model*, that can be readily put into production. The process that turn input to feature is what we call *transform*.

It is very common to preprocess the raw inputs, *e.g.*, transforming them to format/values (features) that are expected by the estimators. Common examples include standardization, min-max scaling (for scalar inputs), ont-hot encoding, embedding (for categorical inputs). To ensure reproducibility, it is suggested to include such preprocessing steps as part of the model. With `sklearn`, one can leverage the [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) class, and with tensorflow/keras, one can use the [`tf.feature_column`](https://www.tensorflow.org/api_docs/python/tf/feature_column) API, to make the preprocessing as part of the computation graph (*i.e.*, model).

The benefit of applying this design pattern is obvious: when put into production, the model will ingest the **raw input**, whereas the preprocessing steps will be encapsulated yet they are part of the model itself. When we deploy a new model, we will be enforced to apply the new preprocessing steps as well. The following figure (from the book) illustrate such pattern, in the context of predicting the duration of a [New York city Citibike](https://en.wikipedia.org/wiki/Citi_Bike) ride:

<figure>
<center>
<a href="/assets/images/mldp_0601.png"><img src="/assets/images/mldp_0601.png"></a>
</center>
</figure>

There are cases in which one can not package the input-to-feature transformation in the model. For example, in the above bicycle duration prediction model, if a feature is "the hour of the day for the previous bike rides from the same station", obviously we need to treat it as a raw input instead something we can "transform". For such cases, the **feature store** design pattern discussed later would be a better approach.

## Bridged Schema

This design pattern aims to address the issue when the training dataset is a hybrid of data conforming to different schema. Assuming that we are training a regression model, and one of the (categorical) input is called `payment_type`. In the older training data, this has been recorded as `cash` or `card`, However, the newer training data provide more detail on the type of card (`gift_card`, `debit_card`, `credit_card`) that was used. During inference, we are expecting the detailed input as well. How to handle the different schemas?

There are two simple solutions, none of which seem to be optimal. One can either discard the older training data, or roll up the newer training data (and for inference) by treating all three different types of card payment as `card`. For the first approach, we lose the training data, and for the second approach, we lose the information hence degrading the model performance (need to validate!). Is there a trade-off?

This is where the Bridged Schema idea comes in. The main idea is that, can we find a representation (schema) for the input (in this example, `payment_type`), that works for both the older and newer data?

### Probabilistic method
With this approach, we effective "impute" the older data. When we see a `payment_type == card` in the order data, we convert it to one of the (`gift_card`, `debit_card`, `credit_card`), with the probability of the observed frequency in the newer data. The assumption here is that the distributions of the imputed input are the same for the older and newer data, which may not hold.

### Static method
With this approach, we one-hot encode the input using the newer data. For the running example, the `payment_type` is one-hot to a 4-dimension vector, as the cardinality is four (for newer data). When we encounter the `payment_type == card` in the older data, we will represent it as `[0, 0.1, 0.3, 0.6]`, where the first `0` corresponds to the cash category, and `(0.1, 0.3, 0.6)` is the hypothetical, observed frequency of (`gift_card`, `debit_card`, `credit_card`) from newer data. Comparing with the probabilistic method, we relax the "same-distribution" assumption, but allow the ML model to learn the relationship.

### Union schema method (don't use)
Similar to the static method, one could propose to set the cardinality of the `payment_type` to five, that is, treating `card` as its own category. Although tempting, this approach is problematic, since we will never see `payment_type == card` during inference.

## Workflow Pipeline
As an ML practitioner, we can often find our daily routine following some or all of the steps outlined in the figure below.

<figure>
<center>
<a href="/assets/images/mldp_0606.png"><img src="/assets/images/mldp_0606.png"></a>
</center>
</figure>

Similar to the recent monolith-versus-microservice discussion in the traditional programming domain, the Workflow Pipeline design pattern aims to isolate and containerize the individual steps, to ensure the portability, scalability and maintainability the ML pipeline.

Another benefit of abstracting and isolating individual steps is that, one can insert "unit tests"

## Feature Store
blah

## Other design patterns
blah

