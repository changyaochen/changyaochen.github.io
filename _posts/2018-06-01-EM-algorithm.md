---
layout: single
title:  "Fitting a Gaussian Mixture"
date:   2018-06-01 12:00:01 -0600
published: false
tag: [algorithm, python]
excerpt: Fitting one single Gaussian distribution is trivial, but how about more than one?
toc: true
toc_label: "Table of Contents"
header:
  teaser: /assets/images/gmm_teaser.jpeg
---

## A little warm up
As a data scientist, we are dealing with various of distribution on almost daily basis. The simplest (and the grandest) is undoubtly the Gaussian (normal) distribution. Let's assume that we draw 10,000 samples of adult american women's weight (in the unit of lb.), shown as the figure below. By looking at it, we have every reason to believe it follows a Gaussian distribution, but we don't know its mean nor its variance, how can we find out?

<figure>
<a href="/assets/images/gmm_single_gaussian.jpg"><img src="/assets/images/gmm_single_gaussian.png"></a>
</figure>

Well, that is easy, we will just use the mean of the 10,000 samples (sample mean) as the mean of the Gaussian distribution (population mean). Similarily, we will use the sample variance as the population variance. The resulting probability density function (pdf) is plotted together with the histogram in green, which shows good agreement. The data are actually generated from a Gaussian distribution with mean of 170, and variance of 25, so our guesses are pretty close. But why this is the right way?

### Maximum likelihood estimation

The reason is called the [maximum likelihood estimation (MLE)](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation). As in most machine learning problems, we want to set up an objective function, and then tweak its parameters to maximize its value. In this case, we want to maximize the **probability** of observing **all** these (10,000) samples, by tweaking the assumed probability distribution's (Gaussian) parameters (mean and variance).
Here, we define the *likelihood function* (with the Gaussian distribution) as: 

$$
\begin{eqnarray}
\mathcal{L}_i(x_i; \theta) &=& P(x_i | \theta) \\
&=& \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x_i - \mu)^2}{2\sigma^2}},
\end{eqnarray}
$$ 

where \\(x_i\\) is the sample under consideration, and \\(\theta\\) represents the parameters of the assumed distribution. In our case of Gaussian distribution, we have \\(\theta = (\mu, \sigma^2)\\). If there are \\(N\\) independent samples, then the objective function, namely, the probability of observing the \\(N\\) samples, \\(\mathcal{L}(X; \theta)\\) is simply the product of all the individual likelihoods:

$$
\begin{eqnarray}
\mathcal{L}(X; \theta) &=& \Pi_{i=1}^{N}\mathcal{L}_i(x_i; \theta)\\
&=& {\Big(\frac{1}{\sqrt{2\pi\sigma^2}}\Big)}^N
    \Pi_{i=1}^{N} e^{-\frac{(x_i - \mu)^2}{2\sigma^2}}. 
\end{eqnarray}
$$ 

In practice, one usually considers the logarithm of the objective function, as \\(\ell(X; \theta) = \ln{\mathcal{L}}(X; \theta)\\), then we transform the objective function to the log-likelihood as :

$$
\begin{eqnarray}
\ell(X; \mu, \sigma^2) &=& -\frac{N}{2}\ln{(2\pi\sigma^2)} 
                    - \Sigma_{i=1}^N\frac{(x_i - \mu)^2}{2\sigma^2}.
\end{eqnarray}
$$

Again, here \\(\theta = (\mu, \sigma^2)\\). To find the maximum of \\(\ell\\),  we bring out our favoriate method to find an extremum, namely, solving \\(\mu, \sigma^2\\) for \\(\partial \ell / \partial \mu = 0, \partial \ell / \partial \sigma^2 = 0\\). This is high-school level calculus, hence we have:

 $$
\begin{eqnarray}
\mu &=& \frac{1}{N}\Sigma_{i=1}^N x_i,\\
\sigma^2 &=& \frac{1}{N} \Sigma_{i=1}^N (x_i - \mu)^2.
\end{eqnarray}
$$

We can further prove that with this values of \\(\mu\\) and \\(\sigma^2\\), we actually have the maximum of \\(\ell(X; \mu, \sigma^2)\\). Therefore, MLE justifies our "fitting" procedure. 

### How about gradient descent
Before we move on, how about that gradient descent method to calculate the maximum value? Sure, we can randomly pick a set of initial values for \\(\mu\\) and \\(\sigma^2\\), and the follow the standard recipe of gradient descent to find the maximal \\(\ell\\) and the corresponding \\(\mu\\) and \\(\sigma^2\\), but then we have to deal with the proper choices of initial values, learning rates (and its decay), etc. I actually tried to implement a vanilla version of gradient descent on this problem, only to manually tune the learning rate to make it coverage, yike! Since we already have such an easy way, why bother?

# Mixture of two Gaussians
blah

