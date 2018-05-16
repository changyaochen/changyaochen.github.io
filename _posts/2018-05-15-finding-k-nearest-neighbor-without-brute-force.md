---
layout: single
title:  "k Nearest Neighbor Search, without brute force"
date:   2018-05-15 12:00:01 -0600
published: false
tag: [algorithm, python]
excerpt: k nearest neighbor search can be time consuming with brute force, how can we do better?
toc: true
toc_label: "Table of Contents"
header:
  teaser: /assets/images/kNN_teaser.jpg
---

## This is an easy task
I was inspired by a co-worker's project to look into this problem. In her particular case, she has two sets of data, let's call them target set \\(T\\) and query set \\(Q\\). Both sets contain data of dimension \\(d\\), and there are \\(M\\) and \\(N\\) samples in \\(Q\\) and \\(S\\), respectively. In essence, we treat the set \\(T\\) as a \\(N \times d\\) matrix. Similarly, the set \\(Q\\) is represented as a \\(M \times d\\) matrix. 

Then here is the task: for each sample \\(q \in Q\\), we want to find out the 5 samples from \\(T\\), such that, no other sample from \\(T\\) has distance between itself and the query point is closer than those 5 samples. In another word, we want to find the 5 nearest neighbors (NN) of \\(q\\) in \\(T\\). the value of 5 here is rather arbitrary, and it can be generalized to k NNs, or be treated as nearest neighbor search (NNS).

Let's consider a very simple case to visualize this problem, that is, take the dimension \\(d\\) as 2. Let's also define the distance between any two samples as the simple Euclidean distance. Therefore, we can *draw* those samples as points in 2-D plane, and the distance between two samples is just, well, *distance*. Furthermore, let's assume \\(M\\) = 1 and \\(N\\) = 100. Then this example is reduced to: given 100 points on a 2-D plane, and a query point \\(q\\), what are 5 nearest points to \\(q\\)? 

One can probably solve this problem in less than 5 minutes, with few lines of `python` codes. Well, *this is an easy task*. Will the code run fast? Let's see. To calculate the Euclidean distance takes \\(O(d)\\) time. For one query point, we will have to calculate the distance between itself and *all* points in \\(T\\), in which there are \\(N\\). So the total time budget for *one* query point is \\(O(dN)\\). If there are \\(M\\) query points, then the total time complexity will be \\(O(dMN)\\): in the end, we are doing a double for-loop. What's more, this is just to find the nearest neighbor (1-NN). What if we want to find the k nearest neighbors (k-NN)? One can simply do the 1-NN *k* times, that is \\(O(dMNk)\\). 

Is this time budget bad? If we are not dealing with high-dimension data, such as natural language problems, then we can say \\(d\\) will be on the order of hundreds. But we might, and should, have a lot of data: both \\(M\\) and \\(N\\) can be in the order of millions. For my colleague's problem, both \\(M\\) and \\(N\\) are both about 100,000. We implemented the naive double for-loop algorithm, and the estimate run time is about 20 days! In our case, \\(d\\) is larger than 2 though. We also should probably use `numpy` more, and vectorize the data better, but still, there must be a better way...

## A small boost
\\(O(dMN\log{k})\\)


## Can't we learn a thing or two?
Let me mentally walk through the double for-loop process. First, we pick a query point from \\(Q\\), can compare it against all the \\(N\\) points in \\(T\\). Next, we are handed with another query point, and dive back to \\(T\\) again. But can we learn anything from the *previous* run, such as, how the points in \\(T\\) are distributed? So when we are presented with a new query point, we can find our way in \\(T\\) more smartly, namely, bypass some points in \\(T\\) altogether?

## Let's make a map (or plant a tree)
It seems what we need is a map of \\(T\\), or algorithmically speaking, a data structure to describe \\(T\\). Of course, someone has solved this problem, and a typical data structure for this instance is called [**k-d tree**](https://en.wikipedia.org/wiki/K-d_tree). Here "k-d" stands for *k*-dimensional. Don't confuse this *k* with the *k* in our k-NN notation. In this post, we use *d* instead to denote the sample dimension, we will stick to this *d* notation, and use *k* as in *k*-NN.

How can make a map? Let's go back to our simple 2-D example: with all the 100 points form \\(T\\) drawn on the *xy*-plane, we can draw a vertical line that seperates them to two partitions, with 50 points on either side. Let's assume this line bisect the *xy*-plane at about \\(x\\) = 0. Then if the query point lies at the far right side, then we *probably* don't have to visit the points on the left-half of the *xy*-plane. 

But *probably* is not good enough, how can we make sure? The key step is to draw a "bounding box" that contains all the points in each space partition. By making such a box, we can also measure the distance between the query point to the bounding box of the left partition. We can keep dividing each partition, until reaching some stopping criterion. For each partition, we will also make the corresponding bounding boxes. In this way, we make a map of \\(T\\), by making a binary tree out of it.

With this piece of information, the query step becomes:

1. Make the "map".
2. Given the query point, find out which partition it is in.
3. Calculate the distance between the query point and all ohter points in the same partition. Remember the closest point, and the minimum distance (or *k* closest ones).
4. Calculate the distance between the query point and the bounding box of the "sibling" partition. If this distance is larger than the minimum distance, then we can skip this "sibling" partition altogether. Otherwise, we will have to visit all the points in this sibling partition, and update the closest point if needed.
5. Once we have done with this sibling partition, we will traverse up along the tree, and then visit the "uncle" partition (and possibly its children). We will keep traverse the same fashion, until all the points in \\(T\\) are covered.

<figure>
<a href="/assets/images/knn_depth_3.jpg"><img src="/assets/images/knn_depth_3.png"></a>
</figure>

Nothing works better than a simple example. Let's recall the 2-D case, as shown in the figure above. Here the k-d tree (or 2-d tree) has a depth of 3, as the space is partitioned by the mean value of alternating dimensions. In this case, the first partition is split with respect to the *x*-dimension, and seperates the *xy*-plane to left and right, with the dark green line. We will make the bounding box for both of the partitions (not shown here). Then for each partition, the next partitions is split with respect to the *y*-dimension, with the split lines shown in light green. Again, we will make 4 bounding boxes. The next split will be taken with respect to the *x*-dimension, on the 4 partitions, with thinner split lines shown in dark green again. Make bounding boxes, 8 of them this time. Now we have reached our pre-specified stopping criterion (depth equals to 3), so we stop, and the last 8 bounding boxes are also shown. Now we have finished the step 1. 

Now we are handed the query point, which is shown in red. We will follow step 2 to 5 as described above, to get the 1 nearest neighbor. In this particular case, it is apparent that we only have to visit the 11 points in the same depth-3 partition as the query point, as opposed to all the 100 points, and the nearest neighbor is the point at the lower left to the query point.

## How fast is it
Yes! We see that by learning something about \\(T\\) by building a k-d tree, can in practice, greatly speed up the query. Actually, on average, the time complexity for one query is \\(O(d\log{N})\\) (hope with the example, this makes intuitive sense). So for the total \\(M\\) query points, the total search time complexity for 1-NN will be \\(O(dM\log{N})\\). This is a huge boost!

How does it work in our case? Of course, the mighty `sklearn` has already taken care of the [API](http://scikit-learn.org/stable/modules/neighbors.html), so we just need to be happy clients. It took only about 10 seconds to get the all the 5 NN for the \\(M\\) samples. Wow!

## There is no free lunch
This is almost too good to be true, and of course it is not. Although we achieved a huge gain in querying time, it also takes time (and space) to build the k-d tree. Roughly speaking, it will take \\(O(N\log{N}\\) time and \\(O(N)\\) to build the k-d tree. This doesn't sound too bad... However, things can get quite ugly in high dimension case (\\(d \sim N\\)). In such case, one might want to consider inexact methods such as [locality-sensitive hashing](https://en.wikipedia.org/wiki/Locality-sensitive_hashing).

While making this post, I got interested in coding up the recursive partition of k-d tree, which leads to the figure shown in the post. You can find the full script [here](https://github.com/changyaochen/changyaochen.github.io/blob/master/assets/notebooks/kNN.ipynb).



