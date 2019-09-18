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

## The basic
The setting is rather straightforward: you need to hire a secetary (or an analyst, a data scientist), and you only have the time/finanical budget to interview **at most** $$N$$ candidates. 

Here comes the crucial twists. **First**, you can only rank all the interviewed candidates ordinally, without any knowledge of their standings in the hidden, total candidate pool. In another word, the best candidate you have seen so far may or may not be the best candidate you can ever interview.  **Second**, after interviewing each candidate, you have to make the hire/no-hire decision right away. If you decide to hire, the whole process is finished, and if you decide to pass on this candidate, you can not go back to him or her again.

The second constraint turns the decision making process more like a bet: although the one you just interviewed is the best so far, but he or she is just the third of 20 candidates you are interviewing, shall you make the hiring call? Is there a non-random strategy one can follow here?

## Look-then-leap
There are many sensible strategies one can propose here, for example, after you have seen but let go a good candidate, if you have seen more than $$x$$ consective candiates than the previous "benchmark", hire the next who is better than the benchmark. However, the simplest strategy here, is the so-called look-then-leap: you just interview the first $$r$$ candidates, without hiring anyone from them. Then starting from the $$(r+1)^\text{th}$$ candidate, hire the first one who is better than the best of the first $$r$$ candiadtes. In essence, the first $$r$$ candidates establish a reference for you to make the final decisions. Of course, if the best among the first $$r$$ candidate happens to be the best among all, then you are luck out, and have to hire the last candidate you interview, assuming you have to hire someone.

Since we are dealing with a stochastic process here, the objective here would be to **maximize probabilty of hiring the best candidate**. Even we have devised the struture of the strategy, there is still the question of what value of $$r$$ to use. To be more general, the value we are interested in is the ratio, $$r/N$$. It turns out the optimal value is the magical $$1/e$$. 

## Seeing is believing

blah
<figure>
<center>
<a href="/assets/images/secretary_problem_numerical.png"><img src="/assets/images/secretary_problem_numerical.png" style="width:80%;"></a>
</center>
</figure>