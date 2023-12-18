---
layout: single
title:  "Large Language Model (LLM) learning notes, part 2"
date:   2023-12-19 12:00:00 -0600
published: false
tag: [machine learning]
toc: true
toc_sticky: true
excerpt: "Learning notes from the Coursera course on Large Language Models (LLMs)"
header:
  teaser: assets/images/transformer_architecture.png
---
LLM, at the simplest level, is a model to "finish sentences".
The model is trained as a supervised learning problem, where the training data
consists inputs as the "unfinished" sentences, and labels as the next token
in the "finished" sentences. For example, a training sample can be:

> Input: "Sir Issac Newton developed"<br>
> Label: "calculus"<br><br>
> Input: "Sir Issac Newton developed calculus and law of"<br>
> Label: "motion"

Note that, starting and end of the sentence are special tokens

## Evaluation metrics

### ROUGE

### BLEU

## Parameter Efficient Fine-Tuning (PEFT)

### LoRA

### Soft prompt tuning
