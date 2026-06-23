# nexus_cluster
A Python-based distributed systems project implementing the Raft consensus algorithm. Built to explore distributed state machines, leader election, fault tolerance, and low-level network communication across a cluster of nodes.

## Features
* **Raft Consensus**: Core implementation of the Raft algorithm, handling remote procedure calls (RPCs) for leader election and log replication (`raft_rpc.py`).
* **Node Management**: Manages individual cluster node lifecycles, states (Leader, Follower, Candidate), and timeouts (`node.py`).
* **Replicated State Machine**: Ensures consistent state transitions and data integrity across the entire distributed cluster (`state_machine.py`).
* **TCP Transport Layer**: Custom TCP-based network module for reliable, continuous inter-node communication (`tcp_transport.py`).
* **Cluster CLI**: A dedicated command-line interface to spin up nodes, monitor cluster health, and interact with the consensus engine (`cluster_cli.py`).

## Build & Run
```bash
# Clone the repository
git clone https://github.com/apollo-2006/nexus_cluster.git
cd nexus_cluster

# Run the cluster command-line interface
python cluster_cli.py
```

## Author
**Abir Deol**
