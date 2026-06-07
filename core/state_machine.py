class StateMachine:
    # initialize the distributed log and key-value store
    def __init__(self):
        self.log = []
        self.commit_index = 0
        self.kv_store = {}

    # append uncommitted entries to the log
    def append_entry(self, term: int, command: str, key: str, value: str):
        entry = {"term": term, "cmd": command, "key": key, "val": value}
        self.log.append(entry)
        return len(self.log) - 1

    # apply committed log entries to the actual database state
    def apply_commits(self, new_commit_index: int):
        while self.commit_index < new_commit_index:
            self.commit_index += 1
            entry = self.log[self.commit_index - 1]

            if entry["cmd"] == "SET":
                self.kv_store[entry["key"]] = entry["val"]

        print(f"state machine updated. current state: {self.kv_store}")