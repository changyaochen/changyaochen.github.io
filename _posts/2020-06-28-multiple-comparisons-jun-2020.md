---
layout: single
title:  "Statistical tests for multiple comparisons"
date:   2020-06-28 12:00:00 -0600
published: false
tag: [statistics]
toc: true
excerpt: blah.  
header:
  teaser: /assets/images/type_I_II_errors.png
---
> Can you also run the comparison along this dimension? 

I believe this is a common question that is asked to a data scientist or data analyst. Say your company has just run an A/B test, aiming to find whether a blue button leads more coversion than a red button. Millions of clicks later, there seems to be no significant difference. Disappointed, the program manager believe we can still draw some meaningful conclusion: maybe the blue button indeed leads to more conversion *among female users*, or *among users from New York*, etc. The below strip from xkcd perfectly capture this spirit.

<figure>
<center>
<a href="/assets/images/significant_xkcd.png"><img src="/assets/images/significant_xkcd.png"></a>
</center>
</figure>

## What is wrong with that
Apparently, there is no magic about green beans. The problem is that we made a type I error, whose probability is quantified by the *p* value. The common practice is reject the null hypothesis (hence accept the alternative hypothesis) only if the *p* value is less than a pre-determined threshold (usually 0.05). However, such routine becomes probalematic when we perform multiple tests on the same dataset. To drive this point home, let's do a simple simulation. 

We first prepare a random vector $$Y$$ that is drawn from a uniform distribution, so that we know the null hypothesis is true.

~~~py
import numpy as np

n_samples = 10000
Y = np.random.random(n_samples)
~~~

Next, let's add some "colors", namely, create a set of random 0/1 covariates, to "describe" the vector $$Y$$. 

~~~py
import pandas as pd

n_trials = 500
X = []
for _ in range(n_trials):
    X.append(np.random.randint(2, size=n_samples))

data = pd.DataFrame(np.array(X).T)
data.rename(columns={c: f'x_{c}' for c in data.columns}, inplace=True)
data['y'] = Y
~~~

With the help of `pandas`, we have the first 5 rows of our dataset shown as below. In total, we have 10000 rows of observations ($$y$$). 

<figure>
<center>
<a href="/assets/images/multiple_comps_dataframe.png"><img src="/assets/images/multiple_comps_dataframe.png"></a>
</center>
</figure>

Since we know exactly how $$y$$ is generated, so no matter which dimension is chosen, we know the null hypothesis is true. However, if we run all 500 comparisons, by virture of the defition of *p* value, we bound to draw some statistically significant conclusions, if we only rely on obtaining small *p* values. 

~~~py
from tqdm import tqdm
from typing import List
from scipy import stats

def multiple_comparisons(data: pd.DataFrame, label='y') -> List[float]:
    """Run multiple t tests."""
    p_values = []
    for c in tqdm(data.columns):
        if c.startswith('y'): 
            continue
        group_a = data[data[c] == 0][label]
        group_b = data[data[c] == 1][label]

        _, p = stats.ttest_ind(group_a, group_b, equal_var=True)
        p_values.append((c, p))
    
    return p_values

p_values = multiple_comparisons(data)
~~~

If we examine the distribution of the 500 *p* values, we will find it to be more or less uniform across [0, 1], as expected. Therefore, if we choose 0.05 as the type I error rate $$\alpha$$, we will make about 25 false discoveries. 

<figure>
<center>
<a href="/assets/images/multiple_comps_p_hist_1.png"><img src="/assets/images/multiple_comps_p_hist_1.png"></a>
</center>
</figure>

## A simple fix: Bonferroni correction
It seems that, when we are conducting a family of tests on the same dataset, the chance of getting false positives becomes larger. To control for that, one needs to be more strict when deeming "statistically significant". The [Bonferroni correction](https://en.wikipedia.org/wiki/Dunn%E2%80%93Bonferroni_correction) is arguable the simplest fix. If there are $$m$$ comparisons carried out, adjust $$\alpha$$ to $$\alpha / m$$. Namely, only when observed a *p* value that is smaller than $$\alpha / m$$, we reject the null hypothesis. 

If we use the Bonferroni correction to our running example, namely, using 0.0001 as the critial value, we will reject 0 tests, as it should. 

~~~py
# bonferroni correction
print('Total number of discoveries is: {:,}'
      .format(sum([x[1] < threshold / n_trials for x in p_values])))
print('Percentage of significant results: {:5.2%}'
      .format(sum([x[1] < threshold / n_trials for x in p_values]) / n_trials))

# Total number of discoveries is: 0
# Percentage of significant results: 0.00%
~~~

## Get the power back: Benjamini–Hochberg procedure
The major disadvantage for the Bonferroni correction is that, it is too *conservative*. It trades the power for the low type I error rate. To illustrate this drawback, let's make half of the 500 comparisons with true difference. 

We simply take the first 250 features, for each of them, whenever there is `1`, we draw a sample from an $$N(1, 1)$$, and add it to `y`. We create 250 independent $$N(1, 1)$$, each of 10000-long, and then multiply this (10000, 250) matrix, element-wise, to the first 250 columns of the dataset. By doing so, when we conduct the comparison along any of the first 250 dimensions, we should get a significant result. 

~~~py
n_true_features = n_trials // 2

offset = np.random.normal(loc=1., size=(n_samples, n_true_features))        
offset_sum = np.multiply(
    offset, 
    data[data.columns[:n_true_features]].values).sum(axis=1)
Y2 = Y + offset_sum

data['y2'] = Y2

p_values = multiple_comparisons(data, label='y2')
~~~

Let's make the histogram of the corresponding *p* values (shown below), we can indeed find about half (259) of comparisons with *p* value less than 0.05. This is exactly what is expected, as 250 + false positives (13 ~ 250 * 0.05) - false negatives (~11, see last section for esitmation).

<figure>
<center>
<a href="/assets/images/multiple_comps_p_hist_2.png"><img src="/assets/images/multiple_comps_p_hist_2.png"></a>
</center>
</figure>

However, if we apply the Bonferroni correction, that uses 0.0001 as the critial value, we will only get 99 siganifiant results: they are all from the first 250 dimensions, so we are not making any false discoveries, at the expense of 151 false negatives. Namely, we have less (statistical) power. 

To get the power back, one can apply the [Benjamini–Hochberg](http://www.math.tau.ac.il/~ybenja/MyPapers/benjamini_hochberg1995.pdf) procedure. The process is rather simple too: once we get all the *p* values from the $$m$$ comparisons, rank them from low to high. Then traverse from the smallest *p* value, and see whether it is smaller $$\frac{i}{m} \alpha$$. Until this condition is not met, all the preceeding comparisons are deem significant. Pictorially, we plot the sorted *p* values, as well as a straight line connection (0, 0) and ($$m$$, $$\alpha$$), all the comparisons below the line are judged as a discovery.

~~~py
# Benjamini–Hochberg procedure
p_values.sort(key=lambda x: x[1])

for i, x in enumerate(p_values):
    if x[1] >= (i + 1) / len(p_values) * threshold:
        break
significant = p_values[:i]
~~~

The figure below shows the result from our running example, and we find 235 significant results, much better than 99 when using the Bonferroni correction. Among the 235 discoveries, there are 9 false positives, hence we are also getting 24 false negatives.

<figure>
<center>
<a href="/assets/images/multiple_comps_p_hist_3.png"><img src="/assets/images/multiple_comps_p_hist_3.png"></a>
</center>
</figure>

By using less strigent, yet simple Benjamini–Hochberg procedure, we recover the statistical power lost from the Bonferroni correction. However, one still needs to check for the [assumptions](https://en.wikipedia.org/wiki/Multiple_comparisons_problem), and exact use cases.

## Estimation of False Negatives
I think this is a bit fun from the brain. Given the way how we create the `Y2` vector, that is, as the sum of a uniform $$\it{U}(0, 1)$$, and 250 modified Normal distribution, with mean of 1 and variance of 1, such that $$Y_2 \sim \it{U}(0, 1) + \sum_{k=1}^{250}Z_k$$. When the alternative hypothesis is true, the expected difference will be 1, but we also want to know its variance. 

Here we will use the formula for variance, as: 

$$
\mathrm{Var}[X] = \mathrm{E}[X^2] - \mathrm{E}[X]^2
$$

Here each of the $$Z_k$$ is independent of each other, so we can conviently calculate the variance of $$\sum_{k=1}^{250}Z_k$$ from $$Z_k$$. Recall that $$Z_k$$ is created as the product a Bernoulli trial with $$p = \frac{1}{2}$$, and a draw from $$\it{N}(1, 1)$$. Hence we have $$\mathrm{E}[Z_k] = 
\frac{1}{2}$$, and $$\mathrm{Var}[Z_k] = \mathrm{E}[Z_k^2] - \mathrm{E}[Z_k]^2$$. In the variance equation, the former can be calculated from the expectation, where we use the fact that $$\mathrm{E}[X^2] = 2$$ for $$X \sim \it{N}(1, 1)$$. This leads to $$\mathrm{Var}[Z_k] = \frac{3}{4}$$. 

Finally, we arrive at $$\mathrm{E}[Y_2] = 250.5$$, and $$\mathrm{Var}[Y_2] = \frac{3}{4} \times 250 + \frac{1}{12}$$. We will use this variance to approximate the variance of both the test groups, and from here, it is just a short derivation to the number of False Negatives, given both the number of total sample (10000), and number of comparisons (250). 

All the above calcuations can be found in this [notebook](https://github.com/changyaochen/changyaochen.github.io/blob/master/assets/notebooks/multiple_comparisons.ipynb).









