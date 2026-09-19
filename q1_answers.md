# Question 1 — Docker Image Size Optimization

## Part 1: Naive image
- Image: `spam-api:naive`
- Size: 440 MB (439,878,195 bytes)
- Image ID: 402060857447
- Test: `/healthz` returned `{"status":"ok"}`, `/predict` returned correct spam/ham labels.

## Part 2: Multi-stage image
- Image: `spam-api:multi`
- Size: 163 MB (163,273,303 bytes)
- Image ID: a65784f81995
- Reduction: (440 - 163) / 440 = 62.95% ≈ 63%
- Test: identical behavior to naive — same curl outputs.

## Part 3: Explanation
[Write your 2-3 sentences here — use the draft from the previous message as a starting point, but make it your own voice and reference the specific things in YOUR build.]