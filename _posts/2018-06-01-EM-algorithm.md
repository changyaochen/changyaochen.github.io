---
layout: single
title:  "Fitting a Mixture of Gaussians"
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
\mathcal{L}(X; \theta) &=& \prod_{i=1}^{N}\mathcal{L}_i(x_i; \theta)
= \prod_{i=1}^{N} P(x_i | \theta) \\
&=& {\Big(\frac{1}{\sqrt{2\pi\sigma^2}}\Big)}^N
    \prod_{i=1}^{N} e^{-\frac{(x_i - \mu)^2}{2\sigma^2}}. 
\end{eqnarray}
$$ 

In practice, one usually considers the logarithm of the objective function, as \\(\ell(X; \theta) = \ln{\mathcal{L}}(X; \theta)\\), then we transform the objective function to the log-likelihood as: <a name="single_gaussian_ll"></a>

$$
\begin{eqnarray}
\ell(X; \mu, \sigma^2) 
&=& \sum_{i=1}^N \ln{P(x_i | \mu, \sigma)} \\
&=& -\frac{N}{2}\ln{(2\pi\sigma^2)} 
                    - \frac{1}{2\sigma^2}\sum_{i=1}^N(x_i - \mu)^2.
\end{eqnarray}
$$

Again, here \\(\theta = (\mu, \sigma^2)\\). To find the maximum of \\(\ell\\),  we bring out our favoriate method to find an extremum, namely, solving \\(\mu, \sigma^2\\) for \\(\partial \ell / \partial \mu = 0, \partial \ell / \partial \sigma^2 = 0\\). This is high-school level calculus, hence we have:

$$
\begin{eqnarray}
\mu &=& \frac{1}{N}\sum_{i=1}^N x_i,\\
\sigma^2 &=& \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2.
\end{eqnarray}
$$

We can further prove that with this values of \\(\mu\\) and \\(\sigma^2\\), we actually have the maximum of \\(\ell(X; \mu, \sigma^2)\\). Therefore, MLE justifies our "fitting" procedure. 

### How about gradient descent
Before we move on, how about that gradient descent method to calculate the maximum value? Sure, we can randomly pick a set of initial values for \\(\mu\\) and \\(\sigma^2\\), and the follow the standard recipe of gradient descent to find the maximal \\(\ell\\) and the corresponding \\(\mu\\) and \\(\sigma^2\\), but then we have to deal with the proper choices of initial values, learning rates (and its decay), etc. I actually tried to implement a vanilla version of gradient descent on this problem, only to manually tune the learning rate to make it coverage, yike! Since we already have such an easy way, why bother?

So what have we learned? Here we are given a set of data (10,000 weights for adult women), and an assumed type of distribution (Gaussian), we are able to "learn" the parameters of the distribution (mean and variance). Therefore, if we are presented with new sample from the same population, we are able to make statistical inference. Really nothing fancy.

## Mixture of two Gaussians
Let's make things a bit more interesting: intead of \\(N\\) = 10,000 weights of adult women, we are given \\(N\\) = 30,000 weights of adult women **and** men, and the histogram of these 30,000 samples looks like the figure below. 

<figure>
<a href="/assets/images/gmm_two_gaussian.jpg"><img src="/assets/images/gmm_two_gaussian.png"></a>
</figure>

Clearly, there are two lumps, and very likely, one is made up mostly by women and the other one by men. Now let's ask this question: *given someone with a weight of 180 lb., how likely this is a male, \\(M\\) (or a female, \\(W\\))?*

### What do we need to learn
The question can be rephrase as, given a data point (\\(x_i\\)), what is the probability that it is drawn from one class (\\(M\\)). Written in equation, we are asking \\(P(M|x_i)\\). Naturally, we like to apply Bayes' rule here:

$$
\begin{eqnarray}
P(M|x_i) 
&=& \frac{P(x_i|M)P(M)}{P(x_i)} \\
&=& \frac{P(x_i|M)P(M)}{P(x_i|M)P(M) + P(x_i|W)P(W)}.
\end{eqnarray}
$$

In order to answer this question, we need to know all the elements in the above equation. Like in the previous case, we assume that both the men's weight and women's weight follow their respective Gaussian distributions, parameterized by \\(\mu_M, \sigma^2_M\\) and \\(\mu_W, \sigma^2_W\\). Once we know that, the likelihood calculation would be straightforward. Furthermore, we need to know the priors, namely, the proportional of each gender (\\(\pi_M = P(M)\\), and \\(\pi_W = P(W)\\)). With these 6 parameters (or 5, since \\(P(M) + P(W) = 1\\)), we can fully describe this mixture of Gaussians. We need to learn **all** of that from the data.

### The objective function

The game plan is still the same: construct a proper objective function that is parameterized by \\(\theta = (\mu_M, \sigma^2_M, \mu_W, \sigma^2_W, \pi_M, \pi_W)\\), and then tweak \\(\theta\\) to maximize the objective function's value. 

Naturally, the objective function is again the (log-)likelihood function, \\(\ell\\), as:

$$
\begin{eqnarray}
\ell(X; \theta) 
&=& \sum_{i=1}^N \ln{P(x_i|\theta)}
= \sum_{i=1}^N \ln{P(x_i|\mu_M, \sigma^2_M, \mu_W, \sigma^2_W, \pi_M, \pi_W)} \\
&=& \sum_{i=1}^N \ln{\big[\pi_M P(x_i|\mu_M, \sigma^2_M) + \pi_W P(x_i|\mu_W, \sigma^2_W)\big]}.
\end{eqnarray}
$$

Well, this is simliar to the [single Gaussian case](#single_gaussian_ll), can we apply the same calculus trick? Not quite... the addition inside the \\(\ln{()}\\) makes things difficult if not impossible. We need a plan B (and hold off the urge of using the vanilla version of the gradient descent).

### The hidden variable
So the addition is the killer, can we get rid of it? What if for each \\(x_i\\), we know its gender (*i.e.*, class), \\(z_i = W\\) or \\(M\\)? If we are geared with such information, then all terms inside the \\(\ln{()}\\) but one will vanish, then we are back into our comfort zone. Then the objective function becomes: <a name="two_gaussian_ll"></a>

$$
\begin{eqnarray}
\ell(X; \theta, Z) 
&=& \sum_{\substack{i=1 \\ z_i=M}}^N \ln{\big[\pi_M P(x_i|\mu_M, \sigma^2_M)\big]}
+ \sum_{\substack{i=1 \\ z_i=W}}^N \ln{\big[\pi_W P(x_i|\mu_W, \sigma^2_W)\big]}\\
&=& \Big(
\sum_{\substack{i=1 \\ z_i=M}}^N \ln{\big[P(x_i|\mu_M, \sigma^2_M)\big]}
+ \sum_{\substack{i=1 \\ z_i=W}}^N \ln{\big[P(x_i|\mu_W, \sigma^2_W)\big]}
\Big) \\ 
&~& + \Big(
\sum_{\substack{i=1 \\ z_i=M}}^N \ln{\pi_M}
+ \sum_{\substack{i=1 \\ z_i=W}}^N \ln{\pi_W}
\Big).
\end{eqnarray}
$$

Hooray! Now we get all the ducks in a row, ready for us to take derivatives, **only if** we know the value of \\(Z\\) (the vectorized \\(z_i\\)). But its value is hidden from us, thus the name of latent variable. To deal with that, we need the EM algorithm, not [Maxwell's EM](https://en.wikipedia.org/wiki/Maxwell%27s_equations), but the Expectation-Maximization. 

Before we move on, let me do some re-orgnization of the symbols, to prevent the equations gets even longer. First let's abstract the gender as class, so we are dealing with 2 classes here, and I will map the subscript \\(M\\) to 1, and \\(W\\) to 2. Next I will introduce the [indicator function](https://en.wikipedia.org/wiki/Indicator_function) \\(\textbf{1}()\\) to make things concise. With this modification, the log-likelihood for our [mixture of two Gaussians](#two_gaussian_ll) becomes:

$$
\begin{eqnarray}
\ell(X; \theta, Z) 
&=&
\sum_{1}^N \sum_{j}^2 \textbf{1}(z_i=j) 
\big(\ln{P(x_i|\mu_j, \sigma^2_j)} + \ln{\pi_j}
\big)
\end{eqnarray}
$$