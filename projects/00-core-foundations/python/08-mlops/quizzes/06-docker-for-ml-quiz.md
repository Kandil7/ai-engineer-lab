# MLops 06: Docker for ML — Quiz

> **Topic Overview**: Containerizing ML workloads — reproducible images, GPU access, and layer caching.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**Why containerize an ML workload?**

- A) To make it slower
- B) To make the environment reproducible across machines
- C) To hide the code
- D) To avoid GPUs

<details><summary>Reveal Answer</summary>

**B.** The image is the environment.

</details>

### Question 2 — Easy

**What does a multi-stage build achieve?**

- A) More layers
- B) A smaller final image by building in one stage and copying artifacts into a lean runtime
- C) Faster training
- D) GPU access

<details><summary>Reveal Answer</summary>

**B.** Build tools stay out of the runtime image.

</details>

### Question 3 — Medium

**How does a container access the GPU?**

- A) Automatically
- B) With the NVIDIA container runtime and a `--gpus` request
- C) It cannot
- D) Via SSH

<details><summary>Reveal Answer</summary>

**B.** GPU access is an explicit runtime configuration.

</details>

### Question 4 — Medium

**Why does layer order matter in a Dockerfile?**

- A) It does not
- B) Caching: dependencies installed before copying code are reused when only code changes
- C) For security
- D) For GPU access

<details><summary>Reveal Answer</summary>

**B.** Ordering controls cache reuse and build time.

</details>

### Question 5 — Medium

**Why avoid `latest` as the base image tag?**

- A) It is slower
- B) It can change under you, breaking reproducibility
- C) It is larger
- D) It lacks a GPU

<details><summary>Reveal Answer</summary>

**B.** Pin the base image.

</details>

### Question 6 — Hard

**A training container OOMs on the GPU but the same code works on the host. Suspects?**

- A) The network
- B) A different CUDA/PyTorch pairing or memory setting in the image, plus the host's VRAM budget
- C) The dataset
- D) The CPU

<details><summary>Reveal Answer</summary>

**B.** The container's runtime differs from the host's.

</details>

### Question 7 — Hard

**Why mount data as a volume instead of copying it into the image?**

- A) For speed of build
- B) Data is large and changes; the image stays small and the data stays external
- C) For security
- D) It is required

<details><summary>Reveal Answer</summary>

**B.** Separate the immutable image from the mutable data.

</details>

### Question 8 — Hard

**Why pin the NVIDIA driver / CUDA compatibility in a GPU image?**

- A) For size
- B) A CUDA build must match the driver and PyTorch build, or kernels fail at runtime
- C) For speed
- D) It is not needed

<details><summary>Reveal Answer</summary>

**B.** Version compatibility is a hard runtime requirement.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can containerize an ML workload. |
| 5-6 | Review GPU access and layer caching. |
| < 5 | Re-read the lecture. |
