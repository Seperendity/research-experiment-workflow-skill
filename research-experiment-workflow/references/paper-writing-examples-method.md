<!-- Adapted from Master-cai/Research-Paper-Writing-Skills (MIT License). See references/paper-writing-attribution.md. -->

Source upstream path: `multiple upstream example files`.

# Paper Writing Examples Method

## Contents

- A. Planning and Writing Workflow
- B. Module Triad and Module-Level Writing
- C. Section-Level Templates
- D. Clarity and Troubleshooting
- Purpose
- Block-by-Block Mapping
  - Section 3.1: Structured Latent Codes
  - Section 3.2: Code Diffusion
  - Section 3.3: Density and Color Regression
  - Section 3.4: Volume Rendering
- Reusable Writing Pattern from This Figure
- Suggested Paragraph Starters

This file flattens the upstream example bank into one reference file so this skill keeps references one level below `references/`.

---

Source upstream path: `research-paper-writing/references/examples/method-examples.md`.

# Method Examples Index

All method example cites should point to the local files below.

## A. Planning and Writing Workflow

1. Pre-writing questions: `references/paper-writing-examples-method.md`

## B. Module Triad and Module-Level Writing

1. Module triad (Neural Body): `references/paper-writing-examples-method.md`
2. Neural Body figure text conversion: `references/paper-writing-examples-method.md`
3. Module design (Instant-NGP): `references/paper-writing-examples-method.md`
4. Module motivation patterns: `references/paper-writing-examples-method.md`

## C. Section-Level Templates

1. Method section skeleton: `references/paper-writing-examples-method.md`
2. Overview template: `references/paper-writing-examples-method.md`
3. Example of the three elements: `references/paper-writing-examples-method.md`

## D. Clarity and Troubleshooting

1. Common issues note: `references/paper-writing-examples-method.md`

---

Source upstream path: `research-paper-writing/references/examples/method/pre-writing-questions.md`.

# Method Pre-Writing Questions


`Before writing Method, answer: (1) what modules exist, and (2) for each module, what is its workflow, why is it needed, and why does it work.`

```text
Questions:
(1) What modules are in the method?
(2) For each module, answer three questions:
    - What is this module's workflow?
    - Why do we need this module?
    - Why does this module work?
```

Recommended action:

1. Organize answers in a mind map or table before writing paragraphs.

---

Source upstream path: `research-paper-writing/references/examples/method/module-triad-neural-body.md`.

# Module Triad Example (Neural Body)

`Use Neural Body to understand the three elements of a module: design, motivation, and technical advantages.`

Local source references:

1. Annotated figure showing motivation/design/advantages split.
3. Text-converted annotation notes: `references/paper-writing-examples-method.md`

Triad mapping template:

1. Module design: what representation/network is built and how forward process runs.
2. Motivation: what unresolved challenge requires this module.
3. Technical advantages: why this module performs better than alternatives.

Direct usage:

1. Read `neural-body-annotated-figure-text.md` to map each paragraph to one triad element.
2. Rebuild your own Method subsection with the same triad order.

---

Source upstream path: `research-paper-writing/references/examples/method/neural-body-annotated-figure-text.md`.

# Neural Body Annotated Figure (Text Conversion)

This file converts the annotated Neural Body figure into reusable writing notes.

## Purpose

Use this mapping to understand how one Method section can explicitly separate:

1. Module motivation
2. Module design (data structure)
3. Module design (forward process)
4. Technical advantages

## Block-by-Block Mapping

### Section 3.1: Structured Latent Codes

1. **Module design (data structure)**
- The paragraph defines structured latent codes anchored to the deformable human model (SMPL).
- It explains what is constructed (latent codes + their anchor positions + frame-dependent transformation by pose).

2. **Technical advantages**
- The paragraph explains why this design works better: dynamic-human representation and cross-frame integration of observations.
- It highlights why anchoring codes to deformable geometry is beneficial.

### Section 3.2: Code Diffusion

1. **Motivation of this module**
- The paragraph states the remaining problem: direct interpolation of sparse structured codes leads to near-zero vectors at many 3D points.
- This motivates diffusion from surface codes to nearby 3D space.

2. **Module design (forward process)**
- The paragraph explains the execution pipeline: build sparse latent volumes, run sparse convolutions, interpolate latent codes at query points, and feed codes to prediction networks.
- This is a canonical input -> steps -> output module description.

### Section 3.3: Density and Color Regression

1. **Module design (forward process) for density model**
- The density paragraph defines how density is regressed from latent code and frame condition.

2. **Module design (data structure) for color model**
- The color paragraph introduces required inputs/embeddings (latent code, view direction, spatial location, temporal embedding).

3. **Module design (forward process) for color model**
- The next paragraph describes how those inputs are encoded and passed into the color MLP for final color prediction.

### Section 3.4: Volume Rendering

1. **Module design (forward process)**
- The paragraph describes ray sampling and volume integration to render image outputs from predicted density/color fields.

## Reusable Writing Pattern from This Figure

For each module subsection, follow this order:

1. `Motivation`: state unresolved challenge and technical reason.
2. `Design-1`: define structure/representation/network.
3. `Design-2`: describe forward process in execution order.
4. `Advantage`: explain why this module improves over alternatives.

## Suggested Paragraph Starters

1. Motivation: `A remaining challenge is ...`
2. Data structure design: `We represent ... with ...`
3. Forward process: `Given [input], we first ... then ... finally ...`
4. Technical advantage: `Compared with previous methods, this design ... because ...`

---

Source upstream path: `research-paper-writing/references/examples/method/module-design-instant-ngp.md`.

# Module Design Example 

This example uses `%` comments as annotations.
Each `% ...` annotation explains the paragraph(s) immediately below it.

```latex
\begin{quote}
\textbf{Annotation rule.} In this example, each line starting with \% labels the role of the paragraph(s) directly below it.
\end{quote}

\begin{itemize}
\item Motivation of this module
\item Module design (data structure)
\item Module design (forward process)
\end{itemize}

\section{3 \quad MULTIRESOLUTION HASH ENCODING}

% Motivation of this module
Given a fully connected neural network \(m(y;\Phi)\), we are interested in an encoding of its inputs \(y=\operatorname{enc}(x;\theta)\) that improves the approximation quality and training speed across a wide range of applications without incurring a notable performance overhead.

% Module design: introduce the module's data structure
Our neural network not only has trainable weight parameters \(\Phi\), but also trainable encoding parameters \(\theta\). These are arranged into \(L\) levels, each containing up to \(T\) feature vectors with dimensionality \(F\). Typical values for these hyperparameters are shown in Table 1. Figure 3 illustrates the steps performed in our multiresolution hash encoding. Each level (two of which are shown as red and blue in the figure) is independent and conceptually stores feature vectors at the vertices of a grid, the resolution of which is chosen to be a geometric progression between the coarsest and finest resolutions \([N_{\min},N_{\max}]\):

\[
N_l := \left\lfloor N_{\min}\cdot b^l \right\rfloor, \tag{2}
\]

\[
b := \exp\!\left(\frac{\ln N_{\max}-\ln N_{\min}}{L-1}\right). \tag{3}
\]

\(N_{\max}\) is chosen to match the finest detail in the training data. Due to the large number of levels \(L\), the growth factor is usually small. Our use cases have \(b\in[1.26,2]\).

% Module design: introduce module design by describing the module forward process
Consider a single level \(l\). The input coordinate \(x\in\mathbb{R}^d\) is scaled by that level's grid resolution before rounding down and up:
\[
\lfloor x_l \rfloor := \lfloor x\cdot N_l \rfloor,\quad
\lceil x_l \rceil := \lceil x\cdot N_l \rceil.
\]

\(\lfloor x_l \rfloor\) and \(\lceil x_l \rceil\) span a voxel with \(2^d\) integer vertices in \(\mathbb{Z}^d\). We map each corner to an entry in the level's respective feature vector array, which has fixed size of at most \(T\). For coarser levels where a dense grid requires fewer than \(T\) parameters, i.e. \((N_l+1)^d \le T\), this mapping is 1:1. At finer levels, we use a hash function \(h:\mathbb{Z}^d\rightarrow\mathbb{Z}_T\) to index into the array, effectively treating it as a hash table, although there is no explicit collision handling. We rely instead on the gradient-based optimization to store appropriate sparse detail in the array, and the subsequent neural network \(m(y;\Phi)\) for collision resolution. The number of trainable encoding parameters \(\theta\) is therefore \(O(T)\) and bounded by \(T\cdot L\cdot F\), which in our case is always \(T\cdot16\cdot2\) (Table 1).

We use a spatial hash function [Teschner et al. 2003] of the form
\[
h(x)=\left(\bigoplus_{i=1}^{d} x_i\pi_i\right)\bmod T, \tag{4}
\]
where \(\oplus\) denotes the bit-wise XOR operation and \(\pi_i\) are unique, large prime numbers. Effectively, this formula XORs the results of a per-dimension linear congruential (pseudo-random) permutation [Lehmer 1951], \emph{decorrelating} the effect of the dimensions on the hashed value. Notably, to achieve (pseudo-)independence, only \(d-1\) of the \(d\) dimensions must be permuted, so we choose \(\pi_1:=1\) for better cache coherence, \(\pi_2=2{,}654{,}435{,}761\), and \(\pi_3=805{,}459{,}861\).

Lastly, the feature vectors at each corner are \(d\)-linearly interpolated according to the relative position of \(x\) within its hypercube, i.e. the interpolation weight is \(w_l := x_l-\lfloor x_l \rfloor\).

Recall that this process takes place independently for each of the \(L\) levels. The interpolated feature vectors of each level, as well as auxiliary inputs \(\xi\in\mathbb{R}^E\) (such as the encoded view direction and textures in neural radiance caching), are concatenated to produce \(y\in\mathbb{R}^{LF+E}\), which is the encoded input \(\operatorname{enc}(x;\theta)\) to the MLP \(m(y;\Phi)\).

\textbf{Performance vs. quality.} Choosing the hash table size \(T\) provides a trade-off between performance, memory and quality. Higher values of \(T\) result in higher quality and lower performance. The memory ...
```

---

Source upstream path: `research-paper-writing/references/examples/method/module-motivation-patterns.md`.

# Module Motivation Writing Patterns


`Module motivation is usually problem-driven: because a problem exists, we design xx to solve it.`

Typical opening sentences:

1. `A remaining problem/challenge is ...`
2. `However, we ...`
3. `Previous methods have difficulty in ...`

Usage note:

1. State the specific failure before introducing the module.
2. Keep motivation independent from implementation details.

---

Source upstream path: `research-paper-writing/references/examples/method/section-skeleton.md`.

# Method Section Skeleton

```latex
\section{Method}
% Overview
% Section 3.1
% Section 3.2
% Section 3.3
```

---

Source upstream path: `research-paper-writing/references/examples/method/overview-template.md`.

# Method Overview Template


`Overview usually includes setting, core contribution, optional figure pointer, and subsection map.`

```latex
% Overview
% One or two sentences for setting
%% Example 1: Given a sparse multi-view video of a performer, our task is to generate a free-viewpoint video of the performer.
%% Example 2: Given an image, the task of pose estimation is to detect objects and estimate their orientations and translations in the 3D space.

% One or two sentences for core contribution
%% Example 1: We build upon prior work for static scenes [46], to which we add the notion of time, and estimate 3D motion by explicitly modeling forward and backward scene flow as dense 3D vector fields.
%% Example 2: Inspired by [21, 25], we perform object segmentation by deforming an initial contour to match object boundary.
%% Example 3: Inspired by recent methods [29, 30, 36], we estimate the object pose using a two-stage pipeline: we first detect 2D object keypoints using CNNs and then compute 6D pose parameters using the PnP algorithm. Our innovation is in a new representation for 2D object keypoints as well as a modified PnP algorithm for pose estimation.

% If pipeline/framework is novel, point to figure
%% Example: The overview of the proposed model is illustrated in Figure 3.

% Explain what Section 3.1 covers
%% Example 1: Neural Body starts from a set of structured latent codes attached to the surface of a deformable human model (Section 3.1).
%% Example 2: In this section, we first describe how to model 3D scenes with MLP maps (Section 3.1).

% Explain what Section 3.2 covers
%% Example 1: The latent code at any location around the surface can be obtained with a code diffusion process (Section 3.2) and then decoded to density and color values by neural networks (Section 3.3).
%% Example 2: Then, Section 3.2 discusses how to represent volumetric videos with dynamic MLP maps.

% Explain what Section 3.3 covers
%% Example 3: Finally, we introduce some strategies to speed up the rendering process (Section 3.3).
```

---

Source upstream path: `research-paper-writing/references/examples/method/example-of-the-three-elements.md`.

# Example of the Three Elements

This example uses `%` comments as annotations.  
Each `% ...` annotation explains the paragraph(s) immediately below it.

```latex
\begin{quote}
\textbf{Annotation rule.} In this example, each line starting with \% labels the role of the paragraph(s) directly below it.
\end{quote}

\begin{itemize}
\item Module design (data structure)
\item Motivation of this module
\item Technical advantages of this module
\item Module design (forward process)
\end{itemize}

\subsection{3.1. Structured latent codes}

% Module design: introduce the module's data structure
To control the spatial locations of latent codes with the human pose, we anchor these latent codes to a deformable human body model (SMPL) [38]. SMPL is a skinned vertex-based model, which is defined as a function of shape parameters, pose parameters, and a rigid transformation relative to the SMPL coordinate system. The function outputs a posed 3D mesh with 6890 vertices. Specifically, we define a set of latent codes \( Z = \{z_1, z_2, ..., z_{6890}\} \) on vertices of the SMPL model. For the frame \( t \), SMPL parameters \( S_t \) are estimated from the multi-view images \( \{I_t^c \mid c = 1, ..., N_c\} \) using [26]. The spatial locations of the latent codes are then transformed based on the human pose \( S_t \) for the density and color regression. Figure 3 shows an example. The dimension of latent code \( z \) is set to 16 in our experiments.

% Technical advantages of this module
Similar to the local implicit representations [25, 5, 18], the latent codes are used with a neural network to represent the local geometry and appearance of a human. Anchoring these codes to a deformable model enables us to represent a dynamic human. With the dynamic human representation, we establish a latent variable model that maps the same set of latent codes to the implicit fields of density and color at different frames, which naturally integrates observations at different frames.

\subsection{3.2. Code diffusion}

% Motivation of this module
Figure 3(a) shows the process of code diffusion. The implicit fields assign the density and color to each point in the 3D space, which requires us to query the latent codes at continuous 3D locations. This can be achieved with the trilinear interpolation. However, since the structured latent codes are relatively sparse in the 3D space, directly interpolating the latent codes leads to zero vectors at most 3D points. To solve this problem, we diffuse the latent codes defined on the surface to nearby 3D space.

% Module design: introduce module design by describing the module forward process
Inspired by [65, 56, 49], we choose the SparseConvNet [21] to efficiently process the structured latent codes, whose architecture is described in Table 1. Specifically, based on the SMPL parameters, we compute the 3D bounding box of the human and divide the box into small voxels with voxel size of \( 5mm \times 5mm \times 5mm \). The latent code of a non-empty voxel is the mean of latent codes of SMPL vertices inside this voxel. SparseConvNet utilizes 3D sparse convolutions to process the input volume and output latent code volumes with \( 2\times, 4\times, 8\times, 16\times \) downsampled sizes. With the convolution and downsampling, the input codes are diffused to nearby space. Following [56], for any point in 3D space, we interpolate the latent codes from multi-scale code volumes of network layers 5, 9, 13, 17, and concatenate them into the final latent code. Since the code diffusion should not be affected by the human position and orientation in the world coordinate system, we transform the code locations to the SMPL coordinate system.

For any point \( \mathbf{x} \) in 3D space, we query its latent code from the latent code volume. Specifically, the point \( \mathbf{x} \) is first transformed to the SMPL coordinate system, which aligns the point and the latent code volume in 3D space. Then, the latent code is computed using the trilinear interpolation. For the SMPL parameters \( S_t \), we denote the latent code at point \( \mathbf{x} \) as \( \psi(\mathbf{x}, Z, S_t) \). The code vector is passed into MLP networks to predict the density and color for point \( \mathbf{x} \).

\subsection{3.3. Density and color regression}

Figure 3(b) overviews the regression of density and color for any point in 3D space. The density and color fields are represented by MLP networks. Details of network architectures are described in the supplementary material.

% Module design: introduce module design by describing the module forward process
\textbf{Density model.} For the frame \( t \), the volume density at point \( \mathbf{x} \) is predicted as a function of only the latent code \( \psi(\mathbf{x}, Z, S_t) \), which is defined as:

\[
\sigma_t(\mathbf{x}) = M_{\sigma}(\psi(\mathbf{x}, Z, S_t)),
\tag{1}
\]

where \( M_{\sigma} \) represents an MLP network with four layers.

% Module design: introduce the module's data structure
\textbf{Color model.} Similar to [37, 44], we take both the latent code \( \psi(\mathbf{x}, Z, S_t) \) and the viewing direction \( \mathbf{d} \) as input for the color regression. To model the location-dependent incident light, the color model also takes the spatial location \( \mathbf{x} \) as input. We observe that temporally-varying factors affect the human appearance, such as secondary lighting and self-shadowing. Inspired by the auto-decoder [48], we assign a latent embedding \( \ell_t \) for each video frame \( t \) to encode the temporally-varying factors.

% Module design: introduce module design by describing the module forward process
Specifically, for the frame \( t \), the color at \( \mathbf{x} \) is predicted as a function of the latent code \( \psi(\mathbf{x}, Z, S_t) \), the viewing direction \( \mathbf{d} \), the spatial location \( \mathbf{x} \), and the latent embedding \( \ell_t \). Following [51, 44], we apply the positional encoding to both the viewing direction \( \mathbf{d} \) and the spatial location \( \mathbf{x} \), which enables better learning of high frequency functions. The color model at frame \( t \) is defined as:

\[
c_t(\mathbf{x}) = M_c(\psi(\mathbf{x}, Z, S_t), \gamma_d(\mathbf{d}), \gamma_x(\mathbf{x}), \ell_t),
\tag{2}
\]

where \( M_c \) represents an MLP network with two layers, and \( \gamma_d \) and \( \gamma_x \) are positional encoding functions for viewing direction and spatial location, respectively. We set the dimension of \( \ell_t \) to 128 in experiments.

\subsection{3.4. Volume rendering}

% Module design: introduce module design by describing the module forward process
Given a viewpoint, we utilize the classical volume rendering techniques to render the Neural Body into a 2D image. The pixel colors are estimated via the volume rendering integral equation [27] that accumulates volume densities and colors along the corresponding camera ray. In practice, the integral is approximated using numerical quadrature [41, 44]. Given a pixel, we first compute its camera ray \( \mathbf{r} \) using the camera parameters and sample \( N_k \) points \( \{\mathbf{x}_k\}_{k=1}^{N_k} \) along camera ray \( \mathbf{r} \) between near and far bounds. The scene bounds are estimated based on the SMPL model. Then, Neural Body predicts volume densities and colors at these points. For the video frame \( t \), the rendered color \( \hat{C}_t(\mathbf{r}) \) ...
```

---

Source upstream path: `research-paper-writing/references/examples/method/method-writing-common-issues-note.md`.

# Method Writing Common Issues (Reference Note)

Original source mentioned in your notes:

1. `Method writing common issues (PDF in your source notes)`

Usage recommendation:

1. Use this reference as a troubleshooting checklist after drafting Method.
2. Prioritize unclear motivation, broken flow, missing implementation details, and inconsistent terms.
