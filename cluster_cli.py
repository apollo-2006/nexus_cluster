import sys
import asyncio
from core.node import RaftNode


# boot the asynchronous cluster node
async def boot_node(node_id: int):
    print(f"\n--- nexus cluster booting: node {node_id} ---")

    # define the cluster topology (hardcoded for prototype)
    cluster_peers = [1, 2, 3, 4, 5]
    cluster_peers.remove(node_id)

    node = RaftNode(node_id, cluster_peers)

    # run the raft daemon indefinitely
    await asyncio.gather(
        node.listen_for_heartbeats()
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("error: node id required. usage: python cluster_cli.py 1")
        sys.exit(1)

    target_id = int(sys.argv[1])
    asyncio.run(boot_node(target_id))