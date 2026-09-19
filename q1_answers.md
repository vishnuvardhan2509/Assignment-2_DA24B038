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





# Question-2

Docker Compose solves single-host, multi-container orchestration: it declares multiple containers — here, the API and Redis — in one YAML file, brings them up together with docker compose up, and automatically provides DNS-based networking so the API reaches Redis by service name (cache) rather than by IP. A single Dockerfile can only build and run one container, so without Compose I would have to manually start Redis, create a Docker network, attach both containers, and wire the hostnames by hand. Kubernetes operates at a different scale entirely: it orchestrates containers across a cluster of machines, handling scheduling, node failures, autoscaling, rolling updates, and persistent storage. Compose is a developer/CI tool for a single host; Kubernetes is a production platform for a fleet.


