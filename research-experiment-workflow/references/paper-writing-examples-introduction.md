<!-- Adapted from Master-cai/Research-Paper-Writing-Skills (MIT License). See references/paper-writing-attribution.md. -->

Source upstream path: `multiple upstream example files`.

# Paper Writing Examples Introduction

## Contents

- A. Task and Application Versions
- B. Technical Challenge Versions
- C. Pipeline-Introduction Versions

This file flattens the upstream example bank into one reference file so this skill keeps references one level below `references/`.

---

Source upstream path: `research-paper-writing/references/examples/introduction-examples.md`.

# Introduction Examples Index

All introduction example cites should point to the local files below.

## A. Task and Application Versions

1. Version 1: `references/paper-writing-examples-introduction.md`
2. Version 2: `references/paper-writing-examples-introduction.md`
3. Version 3: `references/paper-writing-examples-introduction.md`
4. Version 4: `references/paper-writing-examples-introduction.md`

## B. Technical Challenge Versions

1. Version 1 (existing task): `references/paper-writing-examples-introduction.md`
2. Version 2 (existing task + traditional insight backing): `references/paper-writing-examples-introduction.md`
3. Version 3 (novel task): `references/paper-writing-examples-introduction.md`
4. Novel-task decomposition examples: `references/paper-writing-examples-introduction.md`

## C. Pipeline-Introduction Versions

1. Version 1: `references/paper-writing-examples-introduction.md`
2. Version 2: `references/paper-writing-examples-introduction.md`
3. Version 3: `references/paper-writing-examples-introduction.md`
4. Version 4: `references/paper-writing-examples-introduction.md`
5. Not recommended pattern: `references/paper-writing-examples-introduction.md`

---

Source upstream path: `research-paper-writing/references/examples/introduction/version-1-task-then-application.md`.

# Introduction Version 1: Task First, Then Application


`Version 1: If the task is relatively niche, introduce the task first, then introduce applications.`

```latex
% Introduce Task (if the task is very familiar, this part can be skipped)
%% Example: Object pose estimation aims to estimate object's orientation and translation relative to a canonical frame from a single image.
[xxx task] targets at recovering/reconstructing/estimating [xxx output] from [xxx input].

% Introduce Application
%% Example: Accurate pose estimation is essential for a variety of applications such as augmented reality, autonomous driving and robotic manipulation.
[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/version-2-application-first.md`.

# Introduction Version 2: Application First


`Version 2: If the task is already familiar to most readers, introduce applications directly.`

```latex
% Introduce Application
%% Example: Accurate pose estimation is essential for a variety of applications such as augmented reality, autonomous driving and robotic manipulation.
[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/version-3-general-to-specific-setting.md`.

# Introduction Version 3: General Application -> Specific Setting


`Version 3: Introduce applications of the general task first, then introduce the specific task setting. (Personally recommended when the setting is relatively new.)`

```latex
% Introduce applications of the general task
%% Example: Accurate pose estimation is essential for a variety of applications such as augmented reality, autonomous driving and robotic manipulation.
[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].

% Introduce the specific task setting
%% Example: This paper focuses on the specific setting of recovering the 6DoF pose of an object, i.e., rotation and translation in 3D, from a single RGB image of that object.
This paper focuses on the specific setting of recovering/reconstructing/estimating [xxx output] from [xxx input].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/version-4-open-with-challenge.md`.

# Introduction Version 4: Open with Application and Challenge


`Version 4: If the task is familiar, introduce applications directly and expose the target technical challenge in the opening paragraph via previous methods.`

Expert notes (faithful translation):

1. It is often good if the opening paragraph already states what we want to solve.
2. But this style requires suitable conditions and is less common.
3. Usually, several prior-method paragraphs are still needed before the target challenge becomes clear.

```latex
% Introduce Application
%% Example 1: Reconstructing 3D scenes from multi-view images is a cornerstone of many applications such as augmented reality, robotics, and autonomous driving.
%% Example 2: Instance segmentation is the cornerstone of many computer vision tasks, such as video analysis, autonomous driving, and robotic grasping, which require both accuracy and efficiency.

% Use previous methods to expose the target technical challenge
%% Example 1: Given input images, traditional methods [43, 44, 59] generally estimate the depth map for each image based on the multi-view stereo (MVS) algorithms and then fuse estimated depth maps into 3D models. Although these methods achieve successful reconstruction in most cases, they have difficulty in handling low-textured regions, e.g., floors and walls of indoor scenes, due to the unreliable stereo matching in these regions.
%% Example 2: Most of the state-of-the-art instance segmentation methods [18, 27, 5, 19] perform pixel-wise segmentation within a bounding box given by an object detector [36], which may be sensitive to the inaccurate bounding box. Moreover, representing an object shape as dense binary pixels generally results in costly post-processing.
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/technical-challenge-version-1-existing-task.md`.

# Technical Challenge Version 1 (Existing Task, Existing Methods)


`Version 1: For existing tasks with existing methods, discuss the challenge chain from traditional methods to recent methods and finally to the challenge we solve.`

```latex
% Discuss general technical challenges of this task (to lead into recent methods)
%% Example 1: This problem is quite challenging from many perspectives, including object detection under severe occlusions, variations in lighting and appearance, and cluttered background objects.
%% Example 2: This problem is particularly challenging due to the inherent ambiguity on acquiring human geometry, materials and motions from images.
This problem is particularly challenging due to several factors, including [xxx reason], [xxx reason], and [xxx reason].

% Briefly introduce one class of traditional methods, then discuss their technical challenge
%% Example: Traditional methods have shown that pose estimation can be achieved by establishing the correspondences between an object image and the object model.
To overcome these challenges, traditional methods [how they work], [what they achieve].

%% Example: They rely on hand-crafted features, which are not robust to image variations and background clutters.
However, they [technical challenge they face].

% Briefly introduce one class of recent methods 1 (optional), then discuss their challenge
%% Example: Deep learning based methods train end-to-end neural networks that take an image as input and output its corresponding pose.
Recently, [xxx methods] [how they work], [what they achieve].

%% Example: However, generalization remains as an issue, as it is unclear that such end-to-end methods learn sufficient feature representations for pose estimation.
However, they [limitation], because [xxx technical reason].

% Briefly introduce one class of recent methods 2, then discuss their challenge (must lead to our solved challenge)
%% Example: Some recent methods use CNNs to first regress 2D keypoints and then compute 6D pose parameters using the Perspective-n-Point (PnP) algorithm. In other words, the detected keypoints serve as an intermediate representation for pose estimation. Such two-stage approaches achieve state-of-the-art performance, thanks to robust detection of keypoints.
To overcome this challenge, [xxx methods] [how they work], [what they achieve].

%% Example: However, these methods have difficulty in tackling occluded and truncated objects, since part of their keypoints are invisible. Although CNNs may predict these unseen keypoints by memorizing similar patterns, generalization remains difficult.
However, they [limitation], because [xxx technical reason].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/technical-challenge-version-2-existing-task-insight-backed-by-traditional.md`.

# Technical Challenge Version 2 (Existing Task, Insight Backed by Traditional Methods)


`Version 2: For existing tasks, if our technical insight was used in traditional methods, discuss that line to provide conceptual backing.`

```latex
% Introduce one class of traditional/recent methods and discuss their technical challenge (to lead to our insight)
%% Example (Deep Snake): Most of the state-of-the-art instance segmentation methods perform pixel-wise segmentation within a bounding box given by an object detector.
%% Example (ManhattanSDF): Given input images, traditional methods generally estimate the depth map for each image based on the multi-view stereo (MVS) algorithms and then fuse estimated depth maps into 3D models.
Traditional/recent methods [how they work], [what they achieve].

%% Example (Deep Snake): They may be sensitive to the inaccurate bounding box. Moreover, representing an object shape as dense binary pixels generally results in costly post-processing.
%% Example (ManhattanSDF): Although these methods achieve successful reconstruction in most cases, they have difficulty in handling low-textured regions, e.g., floors and walls of indoor scenes, due to the unreliable stereo matching in these regions.
However, they [limitation], because [xxx technical reason].

% Discuss traditional methods that used an insight similar to ours (implicitly backing our idea)
%% Example (Deep Snake): An alternative shape representation is the object contour, which is a set of vertices along the object silhouette. In contrast to pixel-based representation, a contour is not limited within a bounding box and has fewer parameters. Such a contour-based representation has long been used in image segmentation since the seminal work by Kass et al., which is well known as snakes or active contours.
%% Example (ManhattanSDF): To improve the reconstruction of low-textured regions, a typical approach is leveraging the planar prior of manmade scenes, which has long been explored in literature. A renowned example is the Manhattanworld assumption, i.e., the surfaces of man-made scenes should be aligned with three dominant directions.
To overcome this problem, a typical approach is [xxx insight], which has long been explored in literature.

These methods [how they work].

%% Example (Deep Snake): While many variants have been developed in literature, these methods are prone to local optima as the objective functions are handcrafted and typically nonconvex.
%% Example (ManhattanSDF): However, all of them focus on optimizing per-view depth maps instead of the full scene models in 3D space. As a result, depth estimation and plane segmentation could still be inconsistent among views, yielding suboptimal reconstruction quality as demonstrated by our experimental results in Section 5.3.
However, they [limitation], because [xxx technical reason].

% Then discuss newer methods and their remaining challenge (must lead to our solved challenge)
%% Example: There is a recent trend to represent 3D scenes as implicit neural representations and learn the representations from images with differentiable renderers. In particular, [49, 54, 55] use a signed distance field (SDF) to represent the scene and render it into images based on the sphere tracing or volume rendering. Thanks to the well-defined surfaces of SDFs, they recover high-quality 3D geometries from images.
To overcome this challenge, [xxx methods] [how they work], [what they achieve].

%% Example: However, these methods essentially rely on the multi-view photometric consistency to learn the SDFs. So they still suffer from poor performance in low-textured planar regions, as shown in Figure 1, as many plausible solutions may satisfy the photometric constraint in low-textured planar regions.
However, they [limitation], because [xxx technical reason].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/technical-challenge-version-3-novel-task.md`.

# Technical Challenge Version 3 (Novel Task)


`Version 3: For novel tasks without direct methods, define the challenge directly and decompose it by requirement/challenge points.`

```latex
% To achieve xx goal, several requirements/challenges must be satisfied.
%% Example: In this work, our goal is to build a model that captures such object intrinsics from a single image. This problem is challenging for three reasons.

% Describe point 1
%% Example: First, we only have a single image. This makes our work fundamentally different from existing works on 3D-aware image generation models [8, 9, 27, 28], which typically require a large dataset of thousands of instances for training. In comparison, the single image contains at most a few dozen instances, making the inference problem highly under-constrained.

% Describe point 2
%% Example: Second, these already limited instances may vary significantly in pixel values. This is because they have different poses and illumination conditions, but neither of these factors are annotated or known. We also cannot resort to existing tools for pose estimation based on structure from motion, such as COLMAP [35], because the appearance variations violate the assumptions of epipolar geometry.

% Describe point 3
%% Example: Finally, the object intrinsics we aim to infer are probabilistic, not deterministic: no two roses in the natural world are identical, and we want to capture a distribution of their geometry, texture, and material to exploit the underlying multi-view information.
```

See also:
1. `references/paper-writing-examples-introduction.md`

---

Source upstream path: `research-paper-writing/references/examples/introduction/novel-task-challenge-decomposition.md`.

# Introduction Novel-Task Challenge Decomposition


`For novel tasks without direct methods, decompose the challenge into clear requirement/challenge points.`

```latex
% To achieve xx goal, several requirements must be satisfied (or several challenges must be handled).
%% Example: In this work, our goal is to build a model that captures such object intrinsics from a single image. This problem is challenging for three reasons.

% Describe point 1
%% Example: First, we only have a single image. This makes our work fundamentally different from existing works on 3D-aware image generation models [8, 9, 27, 28], which typically require a large dataset of thousands of instances for training. In comparison, the single image contains at most a few dozen instances, making the inference problem highly under-constrained.

% Describe point 2
%% Example: Second, these already limited instances may vary significantly in pixel values. This is because they have different poses and illumination conditions, but neither of these factors are annotated or known. We also cannot resort to existing tools for pose estimation based on structure from motion, such as COLMAP [35], because the appearance variations violate the assumptions of epipolar geometry.

% Describe point 3
%% Example: Finally, the object intrinsics we aim to infer are probabilistic, not deterministic: no two roses in the natural world are identical, and we want to capture a distribution of their geometry, texture, and material to exploit the underlying multi-view information.
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md`.

# Pipeline Version 1 (One Contribution, Multiple Advantages)


`Version 1: One contribution with multiple advantages, and one teaser figure to present the basic idea.`

```latex
% In this paper, we propose a novel framework …
%% Example: In this paper, we introduce a novel implicit neural representation for dynamic humans, named Neural Body, to solve the challenge of novel view synthesis from sparse views.
In this paper, we propose a novel framework/representation, named [method name] for [xxx task].

% Teaser for basic idea
%% Example: The basic idea is illustrated in Figure 2.
The basic idea is illustrated in [xxx Figure].

% One-sentence key novelty/contribution (very important ability)
%% Example: For the implicit fields at different frames, instead of learning them separately, Neural Body generates them from the same set of latent codes.
Our innovation is in [one sentence for key novelty].

% Method details
%% Example: Specifically, we anchor a set of latent codes to the vertices of a deformable human model (SMPL in this work), namely that their spatial locations vary with the human pose. To obtain the 3D representation at a frame, we first transform the code locations based on the human pose, which can be reliably estimated from sparse camera views. Then, a network is designed to regress the density and color for any 3D point based on these latent codes. Both the latent codes and the network are jointly learned from images of all video frames during the reconstruction.
Specifically, [how it works in detail].

% Advantage 1
%% Example: This model is inspired by the latent variable model in statistics, which enables us to effectively integrate observations at different frames.
In contrast to previous methods, [our advantage].

% Advantage 2
%% Example: Another advantage of the proposed method is that the deformable model provides a geometric prior (rough surface location) to enable more efficient learning of implicit fields.
Another advantage of the proposed method is that [another advantage].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/pipeline-version-2-two-contributions.md`.

# Pipeline Version 2 (Two Contributions)


`Version 2: Two contributions, and one teaser figure to present the basic idea.`

```latex
% In this paper, we propose a novel framework …
%% Example: In this paper, we introduce a novel implicit neural representation for dynamic humans, named Neural Body, to solve the challenge of novel view synthesis from sparse views.
In this paper, we propose a novel framework/representation, named [method name] for [xxx task].

% One-sentence key novelty
%% Example: To that end, we propose techniques to represent a given subject with rare token identifiers and fine-tune a pre-trained, diffusion-based text-to-image framework that operates in two steps; generating a low-resolution image from text and subsequently applying super-resolution (SR) diffusion models.
Our innovation is in [one sentence for key novelty].

% Teaser
%% Example: The basic idea is illustrated in Figure 2.
The basic idea is illustrated in [xxx Figure].

% Contribution 1 details
%% Example: We first fine-tune the low-resolution text-to-image model with the input images and text prompts containing a unique identifier followed by the class name of the subject (e.g., “A [V] dog”).
Specifically, [how contribution 1 works].

% Advantage of contribution 1
%% Example: This model is inspired by the latent variable model in statistics, which enables us to effectively integrate observations at different frames.
In contrast to previous methods, [advantage of contribution 1].

% Challenge motivating contribution 2
%% Example: In order to prevent overfitting and language drift [35, 40] that cause the model to associate the class name (e.g., “dog”) with the specific instance
However, [another technical challenge].

% Contribution 2 details
%% Example: we propose an autogenous, class-specific prior preservation loss, which leverages the semantic prior on the class that is embedded in the model, and encourages it to generate diverse instances of the same class as our subject.
Specifically, [how contribution 2 works].
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md`.

# Pipeline Version 3 (New Module on Existing Pipeline)


`Version 3: Build on a prior pipeline and introduce one new module, with a teaser figure for the basic idea.`

```latex
% In this paper, we propose a learning-based snake algorithm, named deep snake, for real-time instance segmentation.

% Inspired by previous methods [21, 25], deep snake takes an initial contour as input and deforms it by regressing vertex-wise offsets.

% Our innovation is introducing the circular convolution for efficient feature learning on a contour, as illustrated in Figure 1.

% We observe that the contour is a cycle graph that consists of a sequence of vertices connected in a closed cycle. Since every vertex has the same degree equal to two, we can apply the standard 1D convolution on the vertex features.

% Considering that the contour is periodic, deep snake introduces the circular convolution, which indicates that an aperiodic function (1D kernel) is convolved in the standard way with a periodic function (features defined on the contour).

% The kernel of circular convolution encodes not only the feature of each vertex but also the relationship among neighboring vertices. In contrast, the generic GCN performs pooling to aggregate information from neighboring vertices. The kernel function in our circular convolution amounts to a learnable aggregation function, which is more expressive and results in better performance than using a generic GCN, as demonstrated by our experimental results in Section 5.2.
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/pipeline-version-4-observation-driven.md`.

# Pipeline Version 4 (Observation-Driven Contribution)


`Version 4: Contribution comes from one important observation. Introduce key innovation first, then intuitive observation as motivation, then method details, then benefits.`

```latex
% In this paper, we propose a learning-based snake algorithm, named deep snake, for real-time instance segmentation.

% Our innovation is introducing the circular convolution for efficient feature learning on a contour, as illustrated in Figure 1.

% We observe that the contour is a cycle graph that consists of a sequence of vertices connected in a closed cycle. Since every vertex has the same degree equal to two, we can apply the standard 1D convolution on the vertex features.

% Considering that the contour is periodic, deep snake introduces the circular convolution, which indicates that an aperiodic function (1D kernel) is convolved in the standard way with a periodic function (features defined on the contour).

% The kernel of circular convolution encodes not only the feature of each vertex but also the relationship among neighboring vertices. In contrast, the generic GCN performs pooling to aggregate information from neighboring vertices. The kernel function in our circular convolution amounts to a learnable aggregation function, which is more expressive and results in better performance than using a generic GCN, as demonstrated by our experimental results in Section 5.2.
```

---

Source upstream path: `research-paper-writing/references/examples/introduction/pipeline-not-recommended-abstract-only.md`.

# Not Recommended: Abstract-Only Method Description in Introduction


`Not recommended: If the method is simple, do not avoid concrete method details in Introduction and only discuss abstract insight to make it look novel.`

Expert note (faithful translation):

1. The craft of this writing template is how to make a simple pipeline look novel.
2. Note: this is not about making the insight look novel, but about making the pipeline steps look novel.
3. In most cases this is not recommended.
4. The better target is to clearly explain how the core contribution is implemented in Introduction.

```latex
% To tackle this problem, we propose a novel 3D GAN training method to generate photo-realistic images irrespective of the viewing angle.

% Introduce key idea
% Our key idea is as follows. To ease the challenging problem of learning photorealistic and multi-view consistent image synthesis, we cast the problem into two subproblems, each of which can be solved more easily.

% Explain why the key idea works, but without concretely discussing the full pipeline (or only discuss abstract benefit)
%% Example: Specifically, we formulate the problem as a combination of two simple discrimination problems, one of which learns to discriminate whether a synthesized image looks real or not, and the other learns to discriminate whether a synthesized image agrees with the camera pose. Unlike the formulations of the previous methods, which try to learn the real image distribution for each pose, or to learn pose estimation, our subproblems are much easier as each of them is analogous to a basic binary classification problem.

% Introduce pipeline modules with new terms but without clearly explaining the full pipeline (or skip concrete pipeline details)
%% Example: Based on this key idea, we propose a dual-branched discriminator, which has two branches for learning photorealism and pose consistency, respectively. As these branches are supervised explicitly for their respective purposes, high-quality images with pose consistency can be produced at each viewing angle, and consequently, the generator creates high-quality images and shapes. (This paragraph does not clearly explain how the pipeline works.)

% Introduce another contribution
%% Example: In addition, we propose a pose-matching loss to give supervision to the discriminator for the pose consistency, by considering a positive pose (i.e., rendering pose or ground truth pose) and a negative pose (i.e., irrelevant pose) for a given image. (This paragraph does not clearly explain how the pipeline works.)

% Explain expected benefit over prior methods
%% Example: For example, the frontal viewpoint is one of the irrelevant poses for a side-view image. As reported in the experiments, this loss helps improve image and shape quality. This can be interpreted as a simplification of a classification problem from a large number of classes into binary, which is composed of positive and negative pairs.
```
