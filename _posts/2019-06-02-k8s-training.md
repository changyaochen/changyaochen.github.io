---
layout: single
title:  "Containers and their orchestration"
date:   2019-06-02 12:00:01 -0600
published: false
tag: [misc]
excerpt: Recap of an excellent 3-day workshop on Docker and Kuberentes.
toc: true
header:
  teaser: /assets/images/docker_teaser.png
---
 
One motto I hold as a data scientist is "the only useful code is production code". It is a daunting thought for someone like me to write production level code, and it is a more frightening thought to put my codes in production, however, if that is some skill one has to learn to become a more efficient data scientist, then let's do it. 

In the past week, We hosted [Jérôme Petazzoni](http://jpetazzo.github.io/) for an excellent 3-day workshop on [Kubernetes](https://en.wikipedia.org/wiki/Kubernetes). Initially I was a little concerned about how much I could actually learn, given my almost non-existing knowledge in DevOps, but Jérôme crafts a very well-paced syllabus, starting from container basics all the way to some advanced Kubernetes operations, with hands-on session throughout. Each of the participant is assigned his/her own AWS EC2 and Kubernetes cluster, so that we can always try out we are just taught. The [slides](https://container.training/intro-selfpaced.yml.html#1) are designed in a clean yet informative manner, one can easily come back and review sections that are glossed over. 

## Why container (Docker)
One of the biggest hurdles between moving your kick-ass algorithm/routine developed on your local laptop (often in the form of a jupyter notebook), and the production environment (*i.e.*, so everyone else can use it) is the "[dependency hell](https://en.wikipedia.org/wiki/Dependency_hell)". I once had to debug a model that I trained two years ago, only to realize the `pandas` version was not compatible with the latest one I have in my current dev environment. It was a gruesome experience to make it finally work. One obvious solution is to take a "snapshot" of the whole dev environment, and duplicate it in the prod environment, so everything will work! Now we are talking along the line of a virtual machine (VM). It would solve the problem all right, but VM can require quite some system resources (CPU, memory, and a full-fledged OS), to serve just the logisitic regression model that you spent 5 seconds training. If someone else needs to run his/her applications, another VM will be needed, with more dedicated system resources (CPU, memory, OS, etc). That seems pretty wasteful. 

Incomes the container. To solve the dependency hell issue, all one needs is to specify are the required packages and their respective versions, together with the codebase. Encapsulate all that essentials as your application, and **share** the system resources with other applications. Such reduction in system resource requirement directly translates to financial savings, be it on-premises hardware investment, or cloud-based billings. For more reasons why container is beneficial, check out [Chapter 1](https://container.training/intro-selfpaced.yml.html#17) of Jérôme's slides. 

While container as a concept can be general, [Docker](https://www.docker.com/) is the most popular implementation of this concept, to the point it almost become synonyms to container. However, there are still some subtle terms, that should be better understood. Before going into the workshop, I found the concepts of container, image, layer quite confusing, until Jérôme showed the following slide, that drives the point home.

<a href="/assets/images/docker_concepts.png"><img src="/assets/images/docker_concepts.png" ></a>

If there is anything I learned from the workshop, that will be it.

## Why orchestration (Kubernetes)
  
Jérôme then guided us through more advance container (Docker) concepts such as volume, network, and docker-compose, and also tricks on optimizing images. The focus, however, quickly swtich to container [orchestration](https://en.wikipedia.org/wiki/Orchestration_(computing)). 

At first, I found the emphasis of orchestration pointless: we already have deployed our applications in the production environment, what else do we need? In leading to the reason behind orchestration, Jérôme gave two examples. 

The first is the capability to dynamically scale the number of workers (containers) of a webiste, whose workload changes periodically. The capability to automatically scale the number of workers could easily save the owner a lot of AWS bills. 

The second example truly convinces me the benefit of orchestration, that is to schedule the system resource for different workloads. Image we have a list of jobs to run on 5 servers, each server has 10 GB of RAM, and each job requires different amount of RAM resource. This resembles a 1D [bin-packing problem](https://en.wikipedia.org/wiki/Bin_packing_problem), and it requires some scheduler (*i.e.,* orchestration) to allocate different jobs on each server. Below we have two of such orchestration, and one could easily argue that the arrangement on the right is better since it can fit another 6 GB job whereas the left one can not. 

<a href="/assets/images/docker_orchestration_1d.png"><img src="/assets/images/docker_orchestration_1d.png" ></a>

A job is more likely to have more than just one system resource requirement, therefore we quickly move to high dimensional bin-packing problem, such as the 3D case illustrated below. This example along would persuade me dive deeper.

<a href="/assets/images/docker_orchestration_3d.png"><img src="/assets/images/docker_orchestration_3d.png" ></a>



