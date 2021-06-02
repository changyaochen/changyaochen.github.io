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

While the greatest and latest ML models or architectures often get the most excitements, putting them into practical use (_i.e._, used by the intended audience) usually takes much more effort. In reality, there won't be pristine data handed to you in a reliable fashion, ready for you to call the `.predict()` method. A lot of things can go wrong, and they will go wrong: missing data, 10 of the 5,000 features suddenly become unavailable, the data is too large to fit in a single machine's memory, the latency is more than 2 seconds, ..., the list goes on and on.

In the grand scheme of things, the ML models only occupy a small portion of the whole ecosystem, that makes the ML models *work*. The figure below sums up this situation quite succinctly ([reference](https://papers.nips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)).
<figure>
<a href="/assets/images/ml_hidden_debt.png"><img src="/assets/images/ml_hidden_debt.png"></a>
</figure>
The gist of MLOps, therefore, it to build the end-to-end pipelines, so that your greatest and latest ML models can finally see the light of the day.

## The ML Project Lifecycle

The general pattern (summarized by Andrew Ng and I can't agree more) is to encapsulate the ML project lifecycle to different components, and define clear interface between different components. Namely, the four components are scoping, data, modeling, deployment (figure screenshot from the course).
<figure>
<a href="/assets/images/mlops_lifecycle.png"><img src="/assets/images/mlops_lifecycle.png"></a>
</figure>

### Scoping
This might be the least technical component, but can be the most difficult step.

*Value of the project*. Not all the projects require a deep learning model, and often not even an ML model to start with. There are inevitable cost associated with developing and deploying ML models, and one needs to be convinced that the (long-term) return outweighs the cost.

More importantly, the value of a ML project usually is to improve the business bottom line, _i.e_, the business metrics. If a ML model achieves out-of-chart technical metrics, but does not move the business needle, it will be hard to get the buy-in from the stakeholders. As such, making good estimations from the technical metrics to the business metrics should be part of this scoping step.

*Feasibility of the project*. On the other end of the spectrum, there are tasks, neither domain experts nor some sophisticated ML models can seemingly tackle. For example, using the historical stock prices, to predict the future price of that given stock will almost certainly lead to, at best, random guesses. There are people trading stocks for living (_e.g._, hedge funds), but their scope won't be as narrow as a **single** stock.

### Data

An ML model is only as good as its training data. Put it differently, garbage in, garbage out. This step is where a real ML project differs most from a Kaggle competition: we are not only the mere consumer of the data, but also the producer and guardian of the data.

*Data quality*. The majority of the ML projects deal with labelled data. However, getting the "correct" label might take more effort than one would expect, especially if there are human involved in making the labels. For example, in object detection problems, different labelers might draw (sometimes drastically) different bounding boxes for the same object. Ensuring the quality of the data (including both features and labels) is a worthy investment, than the most advanced ML model.

*Data pipeline*. It is often the case that the training data will accumulate over time (_e.g._, new clicks on the ads), therefore, a data pipeline is needed to process the influx of data (not necessarily streaming). To this end, one probably needs infrastructure support (_e.g._, Airflow, Spark, Kafka), and some monitoring guardrails to ensure the quality.

As summarized by Andrew Ng: if one is dealing with small data, then make sure the data, especially the labels, are clean. On the other hand, if one is dealing with big data, then investigate efforts on data processing.

### Training

This is the more often discussed component in the ML project lifecycle.

### Deployment