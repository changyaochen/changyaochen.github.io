---
layout: single
title:  "The egg drop problem"
date:   2019-10-17 12:00:01 -0600
published: true
tag: [algorithm, python]
excerpt: Egg drop soups are delicious, dropping eggs can also be fun.
toc: true
header:
  teaser: /assets/images/egg_drop_problem_teaser.jpeg
---
A colleague brought this question yesterday after lunch, and I can't help but get to the bottom of it -- apparently this is a rather famous question, shame on me to only learn it now. If you knew about it, you can still play with it [here](http://www.wisewheels.us/egg_drop).

## The problem
The setting is very simple: you have $$e$$ eggs, and a building with $$n$$ floors. You want to find out what is the highest floor to drop an egg without breaking it. In addition, you want to obtain the answer with as little attempts as possible, **even for the worst-case scenario**. Then, what is the minimal number of drops one needs? 

If $$e$$ = 1, namely, we have only one egg, the solution is pretty straightforward. There is no other choice but trying from the first floor onwards. By doing so, we will **for sure** find out the highest, safe, floor from which the egg will not break: it is the floor right below the one we break the egg. What's the minimal number of drops needed for the worst-case scenario? It will be $$n$$ as the worst-case scenario is the highest safe floor is $$n$$ (or $$n$$ - 1 if the egg breaks from floor $$n$$).

## Two eggs
Things get a lot more interesting with $$e$$ = 2: now we are allowed to be wrong once. Naturally, some kind of binary search strategy comes into mind, however, it won't necessarily easily be the best. For example, if $$n$$ = 100, if the highest safe floor is 49, and we start from floor 50 and break the first egg, it will take another 49 attempts to get to the correct answer, totaling 50 attempts. In contrast, a simple "every-10-floor" strategy will lead to only 14 total attempts, as we will drop at floor 10, 20, 30, 40, 50 (breaks the first egg), 41, 42, 43, 44, 45, 46, 47, 48, 49 (correct answer). 

So it seems that this every-$$k$$-floor strategy is a viable strategy, then what is the number of attempts for the worst-case scenario? The worst-case is for us to jump all the way towards $$n$$, only to find out the egg breaks, and then using the only remaining egg to test every floor in the last interval of size $$k$$ - 1. For $$n$$ floors, the answer would be: $$ n~//~k + (k - 1)$$. If $$n$$ = 100, the answer is 19 (for $$k$$ = 8, 9, 10, 11, 12, 13. 

Can we do better than this strategy? Remember that, if we drop the egg from floor $$k$$ without breaking it, we effectively **waste** one attempt, as for the next jump, we should **discount this "successful" attempt if the worst-case scenario happening in the interval**. Therefore, the size of the next jump should be $$k$$ - 1. Similarly, the size of the jump after should be $$k$$ - 2, and so on. Effectively, we are looking for the smallest integer that satisfies the condition of $$\sum_{i=1}^k i \geq n$$. The solution is rather simple, as $$\lceil \frac{1 + \sqrt{1 + 8n}}{2} \rceil$$. For $$n$$ = 100, the answer is 14. 

## More eggs
Why stops at two eggs? However three, four, or $$e$$ eggs? Now one really has to pull some dynamic programming tricks to get the answer. 

Let's say there are $$n$$ floors, and we have $$e$$ eggs at our disposal. In addition, as in the setting of dynamic programming, we will assume that we already know the solution for $$e$$ -1 eggs, for cases of every $$n$$ floors. Effectively, we know $$V(e - 1, t)$$ for $$t \in [1, n]$$. Now with $$e$$ eggs, let me drop it from a random floor $$k$$ where $$ 1 \leq k \leq n$$. If the egg breaks, then we know the highest safe floor is somewhere below $$k$$, and we can piggyback $$V(e - 1, k - 1)$$ for the answer; if the egg doesn't break, then the highest safe floor above $$k$$, **and we only have $$n-k$$ floors to search, with $$e$$ eggs in hand** -- namely, the solution will be $$V(e, n-k)$$. Converting the above logic to Bellman equation, we have:

$$
\begin{align*}
V(e, n) = &\min_{k}{\large(}1 + \max\{V(e-1, k-1), V(e, n-k)\}{\large)}\\
&\text{for}~k = 1, 2, ..., n.
\end{align*}
$$

At first glance, there seem to be some circular dependencies, as calculating $$V(e, n)$$ requires knowing $$V(e, n-k)$$. However, as $$n-k < n,~ \forall k$$, one could calculate $$V(e, 1)$$ first before $$V(e, 2)$$, and then calculate $$V(e, 3)$$, ..., all the way to finally find out $$V(e, n)$$. 

It is worth noting that, one can use this dynamic programming routine for the two eggs case as well, since $$V(1, n)$$ simply equals $$n$$. But it is still worthwhile to illustrate a different line of thinking for the two eggs case.

 **n \ e**|**1**|**2**|**3**|**5**|**10**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
0|0|0|0|0|0
1|1|1|1|1|1
2|2|2|2|2|2
5|5|3|3|3|3
10|10|4|4|4|4
20|20|6|5|5|5
50|50|10|7|6|6
100|100|14|9|7|7 

The table shows some representative values for some $$n$$ and $$e$$. They are calculated from the script [here](https://github.com/changyaochen/changyaochen.github.io/blob/master/assets/notebooks/egg_drop_problem.py). Note that, for $$e > \log_2{n}$$, the optimal solution is simply the binary search. You can also test it out with different $$n$$ and $$e$$ [here](http://www.wisewheels.us/egg_drop).

## The optimal strategy
In the above process, we simply calculated the optimal value, namely, what's the minimal worst-case scenario drops. What is left out is the exact, step-by-step guidance, on how to achieve this optimal value. 

For the two eggs case, it is relatively simple, as the first attempt will be at floor 14, if the egg breaks, then we try from floor 1 with the remaining egg; if the egg does not break, we will next try floor 27 (= 14 + 13); and then 39 (= 14 + 13 + 12) and so on. This is a relatively simple manual.

For $$e$$ > 2, one needs to do some bookkeeping during the dynamic programming routine. Namely, for $$V(e, n)$$, one also needs to record what is the first-drop floor $$k$$ that leads to the optimal value. From there, one can easily backtrack the step, hence retrieve the optimal strategy.


 


