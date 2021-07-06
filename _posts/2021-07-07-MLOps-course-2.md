---
layout: single
title:  "MLOps course: Data"
date:   2021-07-07 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
excerpt: Summary of Coursera MLOps Course 2.
header:
  teaser: /assets/images/coursera-logo-full-rgb.png
---
blah

* Academic/Research ML vs Production ML
* Feature coverage
* Data collection: avoid bias in data
* Labeling: process labeling (from log) and human labeling
* Data validation:
  * Data skew (distribution)
  * How to validate the data?
    * Check schema: summary statistics, min/max/mean/median, valency/cardinality
    * Check distribution: L-infinity distance
* Feature engineering (It is kinda strange to put feature engineering here...)
  * Feature selection
    * Filter method (Check for correlation), one-shot
    * Wrapper method (iterative process)
    * Embedded method (???)
* Data journey and data storage
  * What are the data versioning tool? DVC, git-LFS
