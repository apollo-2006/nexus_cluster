import asyncio
import random
import time


class RaftNode:
    # initialize the distributed node with a randomized election timeout
    def __init__(self, node_id: int, peers: list[int]):
        self.node_id = node_id
        self.peers = peers
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None

        # random timeout prevents split votes during elections
        self.election_timeout = random.uniform(1.5, 3.0)
        self.last_heartbeat = time.time()

    # monitor the network for leader activity
    async def listen_for_heartbeats(self):
        while True:
            await asyncio.sleep(0.1)

            if self.state == "leader":
                await self.broadcast_heartbeats()
                continue

            elapsed = time.time() - self.last_heartbeat
            if elapsed > self.election_timeout:
                print(f"[node {self.node_id}] leader timeout. initiating election.")
                await self.start_election()

    # transition to candidate and request votes from peers
    async def start_election(self):
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.node_id
        votes_received = 1

        print(f"[node {self.node_id}] term {self.current_term}: requesting votes...")

        # in a real system, these are concurrent rpc network calls
        for peer in self.peers:
            vote_granted = await self.request_vote_rpc(peer)
            if vote_granted:
                votes_received += 1

        # calculate majority consensus
        majority = (len(self.peers) + 1) // 2 + 1
        if votes_received >= majority:
            print(f"[node {self.node_id}] achieved consensus! becoming leader.")
            self.state = "leader"
            await self.broadcast_heartbeats()

    # mock rpc call to a peer node
    async def request_vote_rpc(self, target_node: int) -> bool:
        await asyncio.sleep(0.05)  # simulate network latency
        return True  # assume peer grants vote for prototype

    # leader strictly maintains authority over the cluster
    async def broadcast_heartbeats(self):
        print(f"[node {self.node_id}] broadcasting authority pulses...")
        self.last_heartbeat = time.time()
        await asyncio.sleep(1.0)  # heartbeat interval