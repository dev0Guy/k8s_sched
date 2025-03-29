# Kubernetes Scheduler Framework Simulator

## Overview
The **Kubernetes Scheduler Framework Simulator** is designed to facilitate the training and evaluation of custom Kubernetes schedulers. It supports:

- Training schedulers using historical data from Kubernetes clusters.
- Developing and testing **Deep Reinforcement Learning (DRL) schedulers**.
- Simulating pod scheduling scenarios with real-time feedback from a simulated Kubernetes environment.

This framework integrates with **Prometheus** for metrics collection and enables real-time monitoring of scheduling decisions.

---

## Architecture
The framework follows the architecture described in the diagram:

1. **Scheduler**:
   - Retrieves a list of **pending pods** from the Kubernetes API or a simulated environment.
   - Decides whether to **schedule the pod to a node** or **skip the scheduling step (advance the clock).**
   
2. **Simulator & Kubernetes**:
   - The **simulator** emulates a real Kubernetes cluster and its scheduling dynamics.
   - The **Kubernetes component** mimics real-world scheduling constraints and interactions.

3. **Prometheus Metrics Collection**:
   - **Simulator and Kubernetes** push scheduling-related metrics (e.g., pod placements, node utilization, scheduling delays).
   - **Scheduler** pulls metrics from Prometheus to inform and improve scheduling decisions.

---

## Features
✅ **Train custom schedulers** with historical Kubernetes data.
✅ **Integrate Deep Reinforcement Learning (DRL)** for intelligent scheduling.
✅ **Simulate real-world Kubernetes scheduling scenarios**.
✅ **Monitor scheduling performance** using Prometheus metrics.
✅ **Plug-and-play framework** for testing different scheduling algorithms.

---

## Usage
### 1. Setting Up the Framework
#### Prerequisites:
- **Python 3.8+**
- **Kubernetes Cluster (or Minikube for local testing)**
- **Prometheus** for monitoring
- **Tianshou / Stable-Baselines3 (for DRL-based schedulers)**

### 2. Running the Simulator
```bash
python simulator.py  # Start Kubernetes simulation
python scheduler.py  # Start custom scheduler training
```

### 3. Visualizing Metrics
- Start Prometheus and configure it to scrape metrics from the simulator.
- Open **Grafana** (or Prometheus UI) to visualize pod scheduling performance.

---

## Future Enhancements
🚀 Support for multi-agent DRL scheduling.
🚀 Integration with OpenAI Gym for RL-based benchmarking.
🚀 Advanced node affinity and resource-aware scheduling.

---

## Contributing
Feel free to **open issues and submit PRs** to improve the framework! 🚀

---

## License
This project is licensed under the **MIT License**.

