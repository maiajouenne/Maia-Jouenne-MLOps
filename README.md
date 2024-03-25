# Maia-Jouenne-MLOps
## Introduction

This project demonstrates the deployment of a Streamlit-based data application that visualizes housing market statistics and graphs from housing.csv file. It includes a Prometheus counter to track specific interactions within the app. Read the TODO file for more context.

## Prerequisites
  - Docker
  - Git
  - Make
  - Prometheus

## Steps
1. Start minkube and docker:
```bash
minikube start
eval $(minikube docker-env)
```

2. Initialize the project:
```bash
make prepare
```

3. Run the data application:
```bash
make run
```

4. Monitoring with prometheus:
```bash
prometheus --config.file=prometheus.yaml
```
and go to [local](http://localhost:9000/)http://localhost:9000/
