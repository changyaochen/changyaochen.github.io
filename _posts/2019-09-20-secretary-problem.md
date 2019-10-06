---
layout: single
title:  "The secretary problem"
date:   2019-09-20 12:00:01 -0600
published: false
tag: [algorithm, python]
excerpt: How to maximize your chance to find the best candidate, apartment, or even soulmate, only if the world can be modeled simply.
toc: true
header:
  teaser: /assets/images/secretary_problem_teaser.png
---
I was reading the book [Algorithms to Live By](http://algorithmstoliveby.com/) for the second time recently, and finally decided to take a deeper look of some the questions posted inside. There is no more enticing problem than the first example brought forward by the authors, the [secretary problem](https://en.wikipedia.org/wiki/Secretary_problem).

## The problem
The setting is rather straightforward: you need to hire a secetary (or an analyst, a data scientist), and you only have the time/finanical budget to interview **at most** \\(N\\) candidates. 

Here comes the crucial twists. **First**, you can only rank all the interviewed candidates ordinally, without any knowledge of their standings in the hidden, total candidate pool. In another word, the best candidate you have seen so far may or may not be the best candidate you can ever interview.  **Second**, after interviewing each candidate, you have to make the hire/no-hire decision right away. If you decide to hire, the whole process is finished, and if you decide to pass on this candidate, you can not go back to him or her again.

The second constraint turns the decision making process more like a bet: although the one you just interviewed is the best so far, but he or she is just the third of 20 candidates you are interviewing, shall you make the hiring call? Is there a non-random strategy one can follow here?

## Look-then-leap
There are many sensible strategies one can propose here, for example, after you have seen but let go a good candidate, if you have seen more than \\(x\\) consective candiates than the previous "benchmark", hire the next who is better than the benchmark. However, the simplest strategy here, is the so-called look-then-leap: you just interview the first \\(r\\) candidates, without hiring anyone from them. Then starting from the \\((r+1)^\text{th}\\) candidate, hire the first one who is better than the best of the first \\(r\\) candiadtes. In essence, the first \\(r\\) candidates establish a reference for you to make the final decisions. Of course, if the best among the first \\(r\\) candidate happens to be the best among all, then you are luck out, and have to hire the last candidate you interview, assuming you have to hire someone.

Since we are dealing with a stochastic process here, the objective here would be to **maximize probabilty of hiring the best candidate**. Even we have devised the struture of the strategy, there is still the question of what value of \\(r\\) to use. To be more general, the value we are interested in is the ratio, \\(r/N\\), namely, the proportion of candidates to interview before any hiring decisions. It turns out the optimal value is the magical \\(1/e\\). 

## Seeing is believing

Given the seeming simplicity of this strategy, it is hard to resist the temptation of running the "brute-force" simulations, just to see the probabilities of hiring the best candidates, when using different proportions. It is fairly straightforward to code up, as shown [here](https://github.com/changyaochen/changyaochen.github.io/blob/master/assets/notebooks/secretary_problem.py). 

In the simulation settings, we set \\(N\\) = 1000 (number of total candidates), and let the threshold (\\(\left \lfloor{r / N}\right \rfloor \\)) changes from 0.01 to 0.99 with 0.01 step size. For each threshold, we will permutate the sequence of the incoming candidates for 10,000 times while applying the same strategy. **Only if the best candidate is hired, then we will call the trial a success.** 
<figure>
<center>
<a href="/assets/images/secretary_problem_numerical.png"><img src="/assets/images/secretary_problem_numerical.png" style="width:85%;"></a>
</center>
</figure>
The simulated success rate for each threshold is shown in the figure above. The details can be found in [this notebook](https://github.com/changyaochen/changyaochen.github.io/blob/master/assets/notebooks/secretary_problem.ipynb). The red vertical line corresponds to the value of \\(1/e\\), and the red solid curve shows the result of Equation $$\eqref{eq_integral}$$ (see next section). It fits rather well with the aforementioned theory, that \\(1/e\\) is the best threshold to use for this look-then-leap policy. 

## View from the probability lens
It is intelligently irresponsible not to ask why \\(1/e\\) is the magical answer. It turns out one only has to resort to conditional probability to arrive at the answer. 

Under the look-then-leap policy, the objective function one tries to maximize is the probability of selecting the best candidate \\(P(r; N)\\), where \\(r\\) is the "number of looks", and \\(N\\) is the total number of candidates. Then in mathematical language, we have:

$$
\begin{align*}
P(r; N) 
&= 
\sum_{i=1}^N P(i\text{ is selected}, i \text{ is the best}) \\
&= 
\sum_{i=1}^N P(i\text{ is selected}~|~i\text{ is the best}) ~\times P (i\text{ is the best}).
\end{align*}
$$

We simply assume the last term as $$1/N$$, as the best candidate can be at any location in the $$N$$ sequence, with equal probability. After moving this part out from the summation, we can further expand the remaining part using our policy, as: 

$$
\begin{align*}
~&\sum_{i=1}^N P(i\text{ is selected}~|~i\text{ is the best})\\
=&
\sum_{i=1}^r 0 + \sum_{i=r+1}^N P(i\text{ is selected}~|~i\text{ is the best})\\
=& \sum_{i=r+1}^N \frac{r}{i-1}.
\end{align*}
$$

The zero probability for the first $$r$$ items is quite straightforward: if the best candidate happens to be in the first $$r$$ (*i.e*, $$ i \le r $$), then we are luck out. The interesting part is from the second summation: if the best candidate is not in the first $$i$$, then under our policy, the only condition that it will be picked is that, **the second best candidate in the first $$i-1$$ is in the first $$r$$**, and the probability for this condition is $$r/(i-1)$$. Note that here we only require the second best candidate in the first $$i-1$$, instead of that of the $$N$$ since we are dealing with conditional probability here. The illustration below should help to demonstrate this logic.
<figure>
<center>
<a href="/assets/images/secretary_problem_proba.jpg"><img src="/assets/images/secretary_problem_proba.png" style="width:80%;"></a>
</center>
</figure>
Coming back to $$P(r; N)$$, now we have:

$$
\begin{equation}
P(r; N) = \frac{r}{N} \sum_{i=r+1}^N \frac{1}{i-1} \tag{1}\label{eq_master},
\end{equation}
$$

and the goal will be for a given $$N$$ to find the $$r$$ that maixmize $$P(r; N)$$. However, for the sake of analytical purpose, we want to explore the limit where $$N \rightarrow \infty$$, what's the optimal threshold $$t = r/N$$. By doing so, the summation is converted to the integral as:

$$
\begin{align*}
P(r; N) 
&= p(t) \\
&= t\int_x^1 \frac{1}{x} \text{d}x \\
&= -t \ln(t), \tag{2}\label{eq_integral}
\end{align*}
$$

whose maximum can be easily found at $$t = 1/e$$, with $$p(1/e) = 1/e$$. Not surprisingly, the plot of $$-t \ln(t)$$ agrees nicely with the numerical simulations.

## View from the dynamic programming lens
All the preceding derivations are all nice, **except for** that we already assume the "look-then-leap" strategy is the optimal, whereas one only has to hone in the details. But can one prove the assumption?

Of course one can, just some brain gymnastics exercises. The key here is to properly describe the state of the process. Specifically, we need two numbers in this case: $$r$$ and  $$s$$, where $$r$$ is the number of candidates have seen so far, and $$s$$ is the **apparent** ranking of the **last**, *i.e.,* the $$r^\text{th}$$ candidate. The value function, $$V(r, s)$$ that is being sought here, is the **maximum expected probablity of choosing the absolute best candidate when the state is ($$r, s$$)**. As usual, there are $$N$$ total candidates to be considered.  

After having all the semantics in place, the crucial next step is to derive the logical relation between different states. For a given state of ($$r, s$$), if $$ s \neq 1$$, there is no point of choosing this candidate, since he or she is not even the best among the first $$r$$. Therefore, the logical decision is to move on to the $$(r+1)^\text{th}$$, hoping that will be the best (among the first $$r+1$$). By doing so, the state is changed to ($$r+1, s'$$), since the apparent ranking of the $$(r+1)^\text{th}$$ can be anywhere between $$1$$ and $$r+1$$, with equal probability. 

What if we are in the state of ($$r, 1$$)? Then the $$r^\text{th}$$ candidate is indeed the best among all $$r$$ candidates, shall we make the call and end the search, hoping he or she is also the best among all $$N$$ candidates (with absolute ranking of 1)? If so, then we are golden! However, given that we have only seen $$r$$ candidates out of total of $$N$$, this probability of being this lucky **can not be larger than $$r/N$$**. 

Another decision at this ($$r, 1$$) state is, of course, to keep searching. After seeing one more (the $$(r+1)^\text{th}$$) candidate, one can either recurse back to the same situation, *i.e.*, to arrive at the ($$r+1, 1$$) state, with probability of $$1/(r+1)$$, or arrive at a state of ($$r+1, s$$) where $$s \neq 1$$, with probability of $$r/(r+1)$$. If the latter, after kicking oneself of letting go the $$r^\text{th}$$ candidate, we also want to quantify how unlucky we are. This nicely sets up the Bellman equation for this problem as:

$$
\begin{align*}
V(r, 1) = \max{[
\frac{r}{N}, \frac{1}{r+1}\sum_{s'=1}^{r+1}V(r+1, s')
]}
\end{align*}
$$

The $$1/(r+1)$$ factor in the second term represents that "unlucky" case (forego the previous best candidate only to find a worse one). How about the luck case, namely, we found out that the $$r^\text{th}$$ candidate

## Conclusion
How to make decisions under uncertainties.
