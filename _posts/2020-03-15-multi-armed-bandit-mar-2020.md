---
layout: single
title:  "Multi-armed bandit"
date:   2020-03-17 12:00:00 -0600
published: false
tag: [algorithm, python]
toc: true
excerpt: blah
header:
  teaser: /assets/images/slot_machines.jpg
---
Like many people, when I first learned the concept of machine learning, the first split made is to categorize the problems to supervised and unsupervised, a soundly complete grouping. Since then, I have mostly been dealt with the supervised problems, until the reinforcement learning becomes the hottest kid around the block. 

## Exploration vs exploitation trade-off
For a typical supervised learning problem, one usually trains models on a set of existing dataset (with labels), and then deploy the model to make prediction as new data are flowing in. In essence, the model only "learns" during the training stage, and leverage its knowledge ever since. Unless a new training session is triggered (for example with new training data), we simply keeps exploiting. [how about online method?]

Clearly this is not the ideal, at least not how human "learns". We are constantly updating (training) our knowledge (model), often time through making mistaking when applying existing knowledge to a new situation, just like a new-born baby learning to walk. When asked to make a prediction (or decision), there are usually a handful of options one can choose from (is it a cat or dog, to go left or go right), and one will have to rely on a sysematic framework to make the decision. But every decision will have some consequence (rewards), and we inevitably will reflect whether other decisions could have led to better outcome. If so, when facing a similar situtaion again, we will make a better decision as we have learned from past experience. The hope is that, after enough such trial-ane-error, *i.e*, exploration, we would learn enough about the environment, and then commit ourselves to the best action going forward. 

This learning framework, namley, reinforcement learning, sounds similar to supervised learning, but differs in a subtle yet fundamental manner. Here, when one is "exploring", she is not only collecting the data (with the rewards as labels)

BLAH

## The multi-armed bandit problem
The classic example in reinforcement learning is the multi-armed bandit problem. Although the casino analogy is more well-known, a slightly more mathematical desrciption of the problem could be:
 
> As an agent, at any time instance, you are asked to make one action out from total of \\(k\\) options, each of which will return some numerical reward, according to their respective underlying distributions. The question is, what is the **policy** the agent should apply, such that it will **maximize the total reward in the end**?

### The environment (arms)
It helps to make the problem, especially the "arms", concrete. Below we made a 10-armed environment, in which each arm is a Gaussian distribtion with variance of 1. The mean of each arm, \\(\mu_i\\) where \\(i\\) = 0..9, is drawn from a standard Normal distribution. Below is an example of such an environment. 
<figure>
<center>
<a href="/assets/images/multi_armed_bandit_testbed.png"><img src="/assets/images/multi_armed_bandit_testbed.png"></a>
</center>
</figure>
As an agent, my goal is to achieve the largest long-term reward, and if I know all the 10 distributions, I would pull arm #6 all the time, as it has the largest mean (about 1.58). However, I would not know the underlying distribution, as the question is what policy should I apply, *if I have infinite number of attempts*, in order to end up pulling arm #6 in the long run?

Since I can pull infinite number of times, how about I pull each arm, say, 100 times, and starting from the 1001\\(^{\text{th}}\\) attempt, I will pull the arm that gives the highest average reward (from the 100 trials). By the law of large numbers, I will most likely end up pulling arm #6 in the end, but the previous 1000 pulls (or 900 if discount the times we pull on arm #6) seem quite wasteful. Under such policy, we probably explore too much.

### Greedy and \\(\epsilon\\)-greedy policy
The pursuit to explore less sets up us nicely to the greedy policy. Namely, we will try to assign a value to each arm, say as \\(Q_i\\), and update the our estimate of \\(Q_i\\) each time after we pull arm \\(i\\) and get a reward. When making decision for which arm to pull next, we simply "greedily" pull the one that has the highest value, namely, \\(\text{argmax}_i{Q_i}\\).

A critial step here is to update \\(Q_i\\). The simplest implementation is to use the averaged reward as \\(Q_i\\). Assume that there are only 2 arms, each have been pulled 3 times. Arm #1 gives reward as [3, 4, 3], and arm #2 as [2, 5, 4]. Then our estimate for \\(Q_1\\) will be 3.33, and for \\(Q_2\\) will be 3.67. Therefore, under the greedy policy, for the 7\\(^{\text{th}}\\) pull, we will go with arm #2. Say this time we are not so lucky as arm #2 returns 0, then we have to update our estimate of \\(Q_2\\) to 2.75, such that for the next pull, arm #1 becomes a better option, we just need to update \\(Q_1\\) after the pull. You get the idea. 

But only committed to the arm with the highest value estimate, seems a little bit myopic, as we might be exploiting too much. A natural extension is to allow some exploration, such that when deciding which arm to pull next, with a small probability (\\(\epsilon\\)), we will **not** pull the one with the highest value estimate, but a random different arm. This modification consititute the key idea of the \\(\epsilon\\)-greedy policy, in which we try to strike a balance between the exploration-exploitation trade-off. the value of \\(\epsilon\\) will be a hyper-parameter for the algorithm. 


### Comparision between different policies
Both policies make intuitive sense, but we still need a quantitative framework for comparisons. Enter the power of numerical simulation. Once we have created an artifical environment to use as a testbed, we can put an agent into such environment and deploy the policy of interest,  
<figure>
<center>
<a href="/assets/images/multi_armed_bandit_comparison.png"><img src="/assets/images/multi_armed_bandit_comparison.png"></a>
</center>
</figure>

### Upper confidence bound (UCB) policy
blah







