import json
from typing import Dict, Any, List


class RaftRPC:
    """Constructs the standard RPC payloads defined by the Raft Consensus Algorithm."""

    @staticmethod
    def request_vote(term: int, candidate_id: int, last_log_index: int, last_log_term: int) -> str:
        """Invoked by candidates to gather votes."""
        payload = {
            "rpc_type": "RequestVote",
            "term": term,
            "candidate_id": candidate_id,
            "last_log_index": last_log_index,
            "last_log_term": last_log_term
        }
        return json.dumps(payload)

    @staticmethod
    def append_entries(term: int, leader_id: int, prev_log_index: int,
                       prev_log_term: int, entries: List[Dict], leader_commit: int) -> str:
        """Invoked by leader to replicate log entries and provide heartbeats."""
        payload = {
            "rpc_type": "AppendEntries",
            "term": term,
            "leader_id": leader_id,
            "prev_log_index": prev_log_index,
            "prev_log_term": prev_log_term,
            "entries": entries,
            "leader_commit": leader_commit
        }
        return json.dumps(payload)

    @staticmethod
    def parse(data: bytes) -> Dict[str, Any]:
        """Deserializes incoming byte streams back into Python dictionaries."""
        return json.loads(data.decode('utf-8'))