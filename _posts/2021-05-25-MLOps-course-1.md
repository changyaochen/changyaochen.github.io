---
layout: single
title:  "MLOps course: Introduction"
date:   2021-05-31 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
excerpt: Summary of Coursera MLOps Course 1.
header:
  teaser: /assets/images/coursera-logo-full-rgb.png
---
A machine learning model is only useful when it is in production, however, going from Jupyter Notebook to deployment in the production environment (and running reliably) can take more effort than one expects. "Just give the model to the software engineers" is not a very effective solution. The term [MLOps](https://en.wikipedia.org/wiki/MLOps) (Machine Learning + DevOps) thus describes the processes that bridge this gap. Fittingly, Andrew Ng and the team at DeepLearning.AI has created a [Coursera Specialization](https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops) on this topic, and I was only too quick to take it. Here I want to summarize my takeaways from the first (of the four) course: Introduction to Machine Learning in Production.

## The Big Picture

While the greatest and latest ML models or architectures often get the most excitements, putting them into practical use (_i.e._, used by the intended audience) usually takes much more effort. In reality, there won't be pristine data handed to you in a reliable fashion, ready for you to call the `.predict()` method. A lot of things can go wrong, and they will go wrong: missing data, 10 of the 5,000 features suddenly become unavailable, the data is too large to fit in a single machine's memory, the latency is more than 2 seconds, the list goes on and on. In the grand scheme of things, the ML models only occupy a small portion of the whole ecosystem, that makes the ML models *work*. The figure below sums up this situation quite succinctly ([reference](https://papers.nips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf))
<figure>
<a href="/assets/images/ml_hidden_debt.png"><img src="/assets/images/ml_hidden_debt.png"></a>
</figure>

Four parts: scoping, data, modeling, deployment.

Small data: make sure data, especially labels, are clean.
Big data: investigate efforts on data processing.