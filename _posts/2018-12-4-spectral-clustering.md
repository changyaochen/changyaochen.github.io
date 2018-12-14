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

Note that here we need to have a clear definition of the similarity measure. In the most intuitive point-on-2D-plane example, where we can easily define the Euclidean distance, a Gaussian kernel can be applied to transform the distance measure to the corresponding similarity measure. Since the similarity measure is always valid for all data point pairs, the underlying graph is fully connected. 

A natural way to represent a graph is using [adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix). Since here we are dealing with a undirected graph with non-negative edge weights, the adjacency matrix is real and symmetrical. There is one problem through: how do we determine the diagonal elements of the matrix, namely, the similarity between a vertex and itself? It turns out that, for this problem it doesn't really matter, and for convenience, let's just assign them with 100. It will become clear why this is the case later.

An example will make things much clearer. Below is a simple graph with 6 vertice and 8 edges, with edge weight indicating the similarity between the connecting vertices. It is a little bit conter-intuitive since we are not considering (Euclidean) distance which is visually appealing, but rather the reverse, namely, similarity. Also, if there isn't an edge between two vertice, we consider the similarity to be zero. 

<figure>
<center>
<a href="/assets/images/simple_graph.jpg"><img src="/assets/images/simple_graph.png" style="width:75%;"></a>
</center>
</figure>

Let's construst the adjacency matrix \\(S\\) real quick, as:

$$
S = 
\begin{bmatrix}
100 & 8 & 6 & 1 & 0 & 0 \\ 
8 & 100 & 8 & 0 & 0 & 0 \\
6 & 8 & 100 & 0 & 2 & 0 \\
1 & 0 & 0 & 100 & 8 & 8 \\
0 & 0 & 2 & 8 & 100 & 7 \\
0 & 0 & 0 & 8 & 7 & 100 
\end{bmatrix}.
$$ 

Here I implicitly order the vertices alphabetically. The matrix \\(S\\) is also often denoted as \\(A\\), to reflect that it is the adjacency matrix. At this juncture, we successfully convert the data to a graph, and the corresponding matrix representation. We are going to deal with the *[spectrum](https://en.wikipedia.org/wiki/Spectrum_of_a_matrix)* of a matrix representation of the underlying graph, that is, the matrix's set of eigenvalues together with their multiplicities. In another word, we want to explore the spectrum of the graph.


## Spectral clustering as an optimization problem

Once in the graph land, the clustering problem can be viewed as a graph partition. In the simplest case, in which we want to group the data to 2 clusters, we are effectively looking for a [graph cut](https://en.wikipedia.org/wiki/Cut_(graph_theory)) which partition all the vertices to either set \\(A\\) or set \\(B\\), such that the objective function \\(\mathcal{L}\\): 

$$
\begin{eqnarray}
\mathcal{L}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}\\
\end{eqnarray}
$$

is minimized.

Objective function
$$
\begin{eqnarray}
\mathcal{L}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}\\
\mathcal{L}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}
{\large(}\frac{1}{|A|} + \frac{1}{|B|}{\large)}
\end{eqnarray}
$$ 

However, this matrix \\(S\\) isn't the one we really care about, instead, we want to get the [Laplacian matrix](https://en.wikipedia.org/wiki/Laplacian_matrix), \\(L\\), of the graph, as \\(L = D - S\\). Here \\(D\\) is a simple diagnoal matrix, with \\(d_{ii}\\) equals the sum of \\(i^\text{th}\\) row of \\(S\\). It should become clear now why the values of the diagonal elements of \\(S\\) is irrelavent, since they got cancelled out. As a result, each of the row sum for \\(L\\) is zero. The Laplacian matrix for the simple graph is then:

$$
L = 
\begin{bmatrix}
-15 & 8 & 6 & 1 & 0 & 0 \\ 
8 & -16 & 8 & 0 & 0 & 0 \\
6 & 8 & -16 & 0 & 2 & 0 \\
1 & 0 & 0 & -17 & 8 & 8 \\
0 & 0 & 2 & 8 & -17 & 7 \\
0 & 0 & 0 & 8 & 7 & -15 
\end{bmatrix}.
$$ 
