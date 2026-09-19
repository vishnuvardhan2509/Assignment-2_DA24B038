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













Docker Compose solves single-host, multi-container orchestration — it lets you define several containers (here, the API and Redis) in one YAML file, spin them up together with docker compose up, and give them automatic DNS-based networking so api can reach cache by service name. A single Dockerfile can only build and run one container, so without Compose I'd have to manually start Redis, create a Docker network, attach both containers, and wire the hostnames by hand. Kubernetes, by contrast, is designed for cluster-scale orchestration: it schedules pods across many machines, handles node failures, autoscaling, rolling updates, and persistent storage — far more than Compose attempts. Compose is a developer/CI tool for one host; Kubernetes is a production platform for a fleet.







