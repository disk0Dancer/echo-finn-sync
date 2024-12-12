# Distributed Algorithms: Echo and Finn

This repository contains implementations of two distributed algorithms: **Echo** and **Finn**, designed for process synchronization in distributed systems. 
The communication between processes is facilitated by RabbitMQ, an AMQP-based message broker.

## Algorithms Overview

### 1. Echo Algorithm
- **Purpose**: Synchronization in a tree-like network topology.
- **Description**:
    - An initiator sends a message to all neighbors.
    - Each node forwards the message to its neighbors (excluding the sender).
    - Leaf nodes respond with "echo" messages back to their sender.
    - The algorithm terminates when the initiator receives responses from all neighbors.

### 2. Finn Algorithm
- **Purpose**: Synchronization in arbitrary directed networks.
- **Description**:
    - Each node maintains two sets: \( Inc \) (predecessors) and \( NInc \) (predecessors of neighbors).
    - Messages are exchanged until \( Inc \) equals \( NInc \).
    - The algorithm ensures eventual consistency across the network.

---

## Features
- Uses RabbitMQ for inter-process communication.
- Python implementation.
- Modular structure for easy integration and testing.

---

## Prerequisites


- install RabbitMQ
- install UV
- `make echo` - to run echo algorithm
- `make finn` - to run finn algorithm