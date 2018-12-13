---
layout: single
title:  "Spectral clustering, step by step"
date:   2018-12-16 12:00:01 -0600
published: false
tag: [algorithm, python, physics]
excerpt: blah.
toc: true
header:
  teaser: /assets/images/spectral_clustering_teaser.png
---

I was drawn to this problem from a colleague's project: he needs to cluster some hundreds of thousands of distributions. There are two steps in this process: first, one needs to define how to properly measure the similarity (or equivalently, distance) between two distributions, and second, how to properly perform the clustering. For the former, a modified, symmetric [Kullback–Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) is used, whereas for the latter, he uses [spectral clustering](https://en.wikipedia.org/wiki/Spectral_clustering). Priding myself on knowning a thing or two about spectral analysis from the academic days, I was like, spectral what?

## The spectrum where Time is involved
Let me start from the spectal analysis that I was familiar with. Usually it takes some time series data as input, and convert this time-domain signal to a different representation in frequency domain. Experimentally, the time-domian to frequency-domain conversion is usually carried out numerically by [fast Fourier transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) (FFT). If one has the fortunate to afford a [spectral analyzer](https://en.wikipedia.org/wiki/Spectrum_analyzer), the conversion can be performed with hardware, for example, by [superheterodyne down-mixing](https://en.wikipedia.org/wiki/Superheterodyne_receiver). 

It works best with an example. Think a frictionless [pendulum](https://en.wikipedia.org/wiki/Pendulum): we can either describe its motion by its angle \\(\theta(t)\\), whose value changes with time \\(t\\), or simply describe the essence of the pendulum with its oscillation period (or frequency), which is a fixed value. Both the time-domian and frequency-domain signals carry the same information, but apparently the frequency-domain representation is more concise. One can easily learn more about the underlying system by observing characteristics from the frequency spectrum. This convenience highlights the benefits of spectral analysis, and it is why it has found itself enormously [important](https://en.wikipedia.org/wiki/Spectral_analysis) in scientific research. 

## The spectrum where a graph is involved
Apparently, there is no Time involved in this clustering problem. Instead, here we want to group different data points into different clusters. It is best think this problem in the context of a [graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)): each data point, be it a distribution, a person, or any abstract object, can be treated as vertices of the graph. The similarity between any pair of data points can be treated as the weight of the edge that connects the two vertices.

## Spectral clustering as an optimization problem

Objective function
$$
\begin{eqnarray}
\mathcal{L}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}\\
\mathcal{L}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}
{\large(}\frac{1}{|A|} + \frac{1}{|B|}{\large)}
\end{eqnarray}
$$ 