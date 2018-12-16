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
### The minimum cut 
Once in the graph land, the clustering problem can be viewed as a graph partition problem. In the simplest case, in which we want to group the data to 2 clusters, we are effectively looking for a [graph cut](https://en.wikipedia.org/wiki/Cut_(graph_theory)) which partition all the vertices to two disjoint set of \\(A\\) and \\(B\\), such that the objective function \\(\mathcal{L}\\): 

$$
\begin{eqnarray}
\mathcal{L}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}\\
\end{eqnarray}
$$

is minimized. In another word, we want to minimize the total weights of all the edges that cross the cut. This effectively turns the clustering problem to a [minimum cut](https://en.wikipedia.org/wiki/Minimum_cut) problem, where there are well-developed algorithms. 

### The normalized minimum cut 
However, this minimal cut paradigm does not always work well in real clustering problems (see figure 1 of this [paper](https://people.eecs.berkeley.edu/~malik/papers/SM-ncut.pdf) for an example). Instead, one would rather minimize the following objective function:

$$
\begin{eqnarray}
\mathcal{L}_\text{norm}(A, B) = \sum_{i \in A,~ j \in B} s_{ij}
{\large(}\frac{1}{\text{vol}(A)} + \frac{1}{\text{vol}(B)}{\large)},
\end{eqnarray}
$$ 

where \\(\text{vol}(A) = \sum_{i \in A} d_i\\). Here \\(d_i\\) is the degree of vertex \\(i\\), and \\(\text{vol}(A)\\) can be viewed as a measure of the size of the cluster. This "normalized" version of minimum cut problem will penalize cluster with small size, therefore achieving more balanced clusters. Unfortunately, this normalized minimum cut problem is NP-hard, and one has to resort to the approximate solutions.

## Graph Laplacians

In order to solve for the normalized minimum cut problem, one needs to analyze the [Laplacian matrix](https://en.wikipedia.org/wiki/Laplacian_matrix), \\(L\\), of the graph, as \\(L = D - S\\). Here \\(D\\) is a simple diagnoal matrix, with \\(d_{ii}\\) equals the sum of \\(i^\text{th}\\) row of \\(S\\). It should become clear now why the values of the diagonal elements of \\(S\\) is irrelavent, since they got cancelled out. As a result, each of the row sum for \\(L\\) is zero. As the frequency spectrum of a frictionless pendulum can reveal the essence of the motion, the eigenvalues and eigenvectors of the graph Laplacian will guide us to uncover the basic properties of the graph.

The Laplacian matrix for the simple graph is then:

$$
L = 
\begin{bmatrix}
15 & -8 & -6 & -1 & 0 & 0 \\ 
-8 & 16 & -8 & 0 & 0 & 0 \\
-6 & -8 & 16 & 0 & -2 & 0 \\
-1 & 0 & 0 & 17 & -8 & -8 \\
0 & 0 & -2 & -8 & 17 & -7 \\
0 & 0 & 0 & -8 & -7 & 15 
\end{bmatrix}.
$$ 

From here, things start to diverge, in three major directions. One can either proceed with the Graph Laplacian as it is; or one can normalize \\(L\\), in two different ways, as:

$$
\begin{eqnarray}
L_\text{sym} &=& D^{-1/2} L D^{1/2},\\
L_\text{rw} &=& D^{-1} L,
\end{eqnarray}
$$ 

where the subscript \\(\text{sym}\\) and \\(\text{rw}\\) mean symmetric and random walk, respectively. Depending on which graph Laplacian is used, the clustering algorithm differs slightly in the details. In below, I will follow the algorithm proposed in [Ng, Jordan, and Weiss (2002)](https://ai.stanford.edu/~ang/papers/nips01-spectral.pdf), by using \\(L_\text{sym}\\) to perform the clustering task.

## Spectral clustering, step by step

After laying out all the notations, we are finally ready to carry out the \\(k\\)-group clustering with the following steps:

1. Obtain the graph Laplacian as \\(L = S – D\\);
2. Normalize the graph Laplacian as: \\(L_\text{sym} = D^{-1/2} L D^{1/2}\\);
3. Get eigenvalues and eigenvetors of \\(L_\text{sym}\\), with the ascending order of eigenvalues;
4. Take the first \\(k\\) eigenvectors, and to form a \\(N \times k\\) matrix \\(U\\);
5. Form a matrix \\(T\\) from \\(U\\) by normalizing the rows of \\(U\\) to norm 1.
6. Treat each row of \\(T\\) as a data point, run some simple clustering algorithm such as K-means, make cluster assignements (1 to \\(k\\));
7. The original problem will be given the same cluster assignment.

It is worthwhile to go back to the running example, and carry it through the steps. The calculated \\(L_\text{sym}\\) is:

$$
L_\text{sym} = 
\begin{bmatrix}
 0.130 & -0.069 & -0.051 & -0.008 &  0.    &  0.    \\
-0.069 &  0.137 & -0.068 &  0.    &  0.    &  0.    \\
-0.051 & -0.068 &  0.137 &  0.    & -0.017 &  0.    \\
-0.008 &  0.    &  0.    &  0.145 & -0.068 & -0.068 \\
 0.    &  0.    & -0.017 & -0.068 &  0.145 & -0.060 \\
 0.    &  0.    &  0.    & -0.068 & -0.060 &  0.130 \\
\end{bmatrix},
$$

and the corresponding \\(T\\) (with \\(k\\) = 2) is:

$$
T = 
\begin{bmatrix}
0.706 & -0.708 \\
0.677 & -0.735 \\
0.738 & -0.674 \\
0.710 &  0.703 \\
0.740 &  0.672 \\
0.677 &  0.735 \\
\end{bmatrix}.
$$

At this point, without running a formal clustering algorithm, we can easily eyeball that the first three rows (vertices A, B, C) are in a different group than the bottom three rows (vertices D, E, F). 

How does it work in more realistic problems? Taking a page from [scikit-learn's examples](http://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html), I used three of the datasets, and applied the aforementioned steps for spectral clustering (codes [here](http://nbviewer.jupyter.org/github/changyaochen/changyaochen.github.io/blob/master/assets/notebooks/spectral_clustering.ipynb)), and the results look pretty good.

<figure class="third">
<a href="/assets/images/spectral_clustering_moon.png"><img src="/assets/images/spectral_clustering_moon.png" ></a>
<a href="/assets/images/spectral_clustering_moon.blob"><img src="/assets/images/spectral_clustering_blob.png"></a>
<a href="/assets/images/spectral_clustering_aniso.png"><img src="/assets/images/spectral_clustering_aniso.png"></a>
</figure>



