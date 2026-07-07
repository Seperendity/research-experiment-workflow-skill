<!-- Adapted from Master-cai/Research-Paper-Writing-Skills (MIT License). See references/paper-writing-attribution.md. -->

Source upstream path: `multiple upstream example files`.

# Paper Writing Examples Abstract

## Contents

- Reusable skeleton
- Given example pattern 2
- Given example pattern (Deep Snake style from your text)

This file flattens the upstream example bank into one reference file so this skill keeps references one level below `references/`.

---

Source upstream path: `research-paper-writing/references/examples/abstract-examples.md`.

# Abstract Examples Index

All abstract example cites should point to the local files below.

1. Version 1 (Challenge -> Contribution)
`Version 1: Introduce the technical challenge, then use one to two sentences to present the technical contribution that solves the challenge.`
`references/paper-writing-examples-abstract.md`
2. Version 2 (Challenge -> Insight -> Contribution)
`Version 2: Introduce the technical challenge, then use one to two sentences to present the insight for solving the challenge, and then one sentence to present the technical contribution that implements this insight. (Personally recommended.)`
`references/paper-writing-examples-abstract.md`
3. Version 3 (Multiple Contributions)
`Version 3: When there are multiple technical contributions, describe each contribution together with its technical advantage.`
`references/paper-writing-examples-abstract.md`

---

Source upstream path: `research-paper-writing/references/examples/abstract/template-a.md`.

# Abstract Template A Examples (Challenge -> Contribution)

Source scope: your original notes, "Version 1".

```latex
\section{Abstract}
% Task
% Technical challenge for previous methods (discuss around the technical challenge that we solved)
% Introduce the technical contribution for solving the challenge in one to two sentences (usually mention the technical term/name only, without describing every detailed step. The term should be easy to understand and should not create a jump in reading. This ability is very important for writing a good abstract.)
% Introduce the benefits of the technical contribution
% Experiment
```

## Reusable skeleton

1. `[Task sentence]`
2. `However, previous methods suffer from [technical challenge].`
3. `To solve this challenge, we propose [technical contribution name].`
4. `[One more contribution sentence if needed].`
5. `This contribution brings [technical benefit].`
6. `Experiments show [main result].`

---

Source upstream path: `research-paper-writing/references/examples/abstract/template-b.md`.

# Abstract Template B Examples (Challenge -> Insight -> Contribution)

```latex
\section{Abstract}
% Task
%% Example 1: In recent years, generative models have undergone significant advancement due to the success of diffusion models.
%% Example 2: This paper addresses the challenge of novel view synthesis for a human performer from a very sparse set of camera views.

% Technical challenge for previous methods (discuss around the technical challenge that we solved)
%% Example 1: The success of these models is often attributed to their use of guidance techniques, such as classifier and classifier-free methods, which provides effective mechanisms to tradeoff between fidelity and diversity. However, these methods are not capable of guiding a generated image to be aware of its geometric configuration, e.g., depth, which hinders the application of diffusion models to areas that require a certain level of depth awareness.
%% Example 2: Some recent works have shown that learning implicit neural representations of 3D scenes achieves remarkable view synthesis quality given dense input views. However, the representation learning will be ill-posed if the views are highly sparse.

% Introduce the insight for solving the challenge in one sentence
%% Example 1: To address this limitation, we propose a novel guidance approach for diffusion models that uses estimated depth information derived from the rich intermediate representations of diffusion models.
%% Example 2: To solve this ill-posed problem, our key idea is to integrate observations over video frames.

% Introduce the technical contribution that implements the insight in one to two sentences (usually mention the technical term/name only, without describing every detailed step. The term should be easy to understand and should not create a jump in reading. This ability is very important for writing a good abstract.)
%% Example 1: To do this, we first present a label-efficient depth estimation framework using the internal representations of diffusion models. At the sampling phase, we utilize two guidance techniques to self-condition the generated image using the estimated depth map, the first of which uses pseudo-labeling, and the subsequent one uses a depth-domain diffusion prior.
%% Example 2: To this end, we propose Neural Body, a new human body representation which assumes that the learned neural representations at different frames share the same set of latent codes anchored to a deformable mesh

% Introduce the benefits of technical novelty
%% Example 2: so that the observations across frames can be naturally integrated. The deformable mesh also provides geometric guidance for the network to learn 3D representations more efficiently.

% Experiment
```

## Given example pattern 2

1. `This paper addresses the challenge of novel view synthesis for a human performer from a very sparse set of camera views.`
2. `... representation learning will be ill-posed if the views are highly sparse.`
3. `To solve this ill-posed problem, our key idea is to integrate observations over video frames.`
4. `To this end, we propose Neural Body ...`
5. `... observations across frames can be naturally integrated ... provides geometric guidance ...`
6. `Experiments show [main result].`

---

Source upstream path: `research-paper-writing/references/examples/abstract/template-c.md`.

# Abstract Template C Examples (Multiple Contributions)

```latex
% Task
%% This paper introduces a novel contour-based approach named deep snake for real-time instance segmentation.

%% Unlike some recent methods that directly regress the coordinates of the object boundary points from an image

% Introduce technical contribution and technical advantage in one sentence (this ability is very important for writing a good abstract.)
%% deep snake uses a neural network to iteratively deform an initial contour to match the object boundary, which implements the classic idea of snake algorithms with a learning-based approach.

% Introduce technical contribution and technical advantage in one sentence
%% For structured feature learning on the contour, we propose to use circular convolution in deep snake, which better exploits the cycle-graph structure of a contour compared against generic graph convolution.

% Introduce technical contribution and technical advantage in one sentence
%% Based on deep snake, we develop a two-stage pipeline for instance segmentation: initial contour proposal and contour deformation, which can handle errors in object localization.

% Experiment
```

## Given example pattern (Deep Snake style from your text)

1. `This paper introduces a novel contour-based approach named deep snake for real-time instance segmentation.`
2. `Unlike some recent methods that directly regress the coordinates of the object boundary points from an image ...`
3. `deep snake uses a neural network to iteratively deform an initial contour ...`
4. `For structured feature learning on the contour, we propose circular convolution ...`
5. `Based on deep snake, we develop a two-stage pipeline ...`
6. `Experiments show [main result].`
