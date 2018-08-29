---
layout: single
title:  "Gradient descent with the right step"
date:   2018-08-30 12:00:01 -0600
published: false
tag: [algorithm, python]
excerpt: Gradient descent is one of the most important tools in machine learning, but how hard can it be?
toc: true
header:
  teaser: /assets/images/gd_teaser.jpg
---

The central theme for many machine learning task is to minmize (or maximize) some objective function \\(f(\theta)\\), often consists of a loss function term and a regularization function term. Well, how hard is it to find the minimum value for \\(f(\theta)\\), just get the first derivate, *i.e.,* gradient \\(\nabla f(\theta)\\), set it to zero, and solve for the magical \\(\theta_\text{magical}\\) such that \\(\nabla f(\theta_\text{magical}) = 0\\), problem solved! Only can it be so easy. In many (if not most) cases, there is no analytical solution for \\(\nabla f(\theta) = 0\\), therefore we want to use some other means to find the minimum of \\(f(\theta)\\), and gradient descent is our best choice. 

### How does gradient descent work

Recall [Taylor expansion](https://en.wikipedia.org/wiki/Taylor_series) for our \\(f(\theta)\\), at a given point \\(\theta_0\\): 

$$
\begin{eqnarray}
f(\theta) = f(\theta_0) ~+~ \nabla f(\theta_0) \Delta \theta ~+~ ...,
\end{eqnarray}
$$ 

where \\(\Delta \theta = \theta - \theta_0\\). If we already know the value of \\(\theta_0\\), hence \\(f(\theta_0)\\), what value of \\(\Delta \theta\\) I should use, such that I can *almost* sure that \\(f(\theta_0 + \Delta \theta)\\) will be smaller than \\(f(\theta_0)\\)? If I can always achieve this goal, at any \\(\theta\\), then I **will** get to the minimum of \\(f(\theta)\\), I just have to! Staring at the Taylor expansion for a while, you can easily find that, if I set \\(\Delta \theta\\) to \\(-\nabla f(\theta_0)\\), or \\(-\eta \nabla f(\theta_0)\\) with \\(\eta > 0\\), then I will have:

$$
\begin{eqnarray}
f(\theta_0 + \Delta \theta) = f(\theta_0) ~-~ \eta (\nabla f(\theta_0))^2 ~+~ ....
\end{eqnarray}
$$ 

If I just ignore the higher order terms, then I got what I wanted: \\(f(\theta_0 + \Delta \theta)\\) will be smaller than \\(f(\theta_0)\\). The key is find the right \\(\Delta \theta\\): clearly, \\(\nabla f(\theta_0)\\) is the gradient at \\(\theta_0\\), and the parameter \\(\eta\\) is usually called step size, or learning rate. There you have it: gradient descent can be clearly understood through the lens of Taylor expansion.

### Backtracking line search
<figure>
<a href="/assets/images/gd_1d.gif"><img src="/assets/images/gd_1d.gif"></a>
</figure>

<figure>
<a href="/assets/images/gd_2d.gif"><img src="/assets/images/gd_2d.gif"></a>
</figure>