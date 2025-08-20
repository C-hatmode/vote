import hashlib, json, time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0", vote_data="Genesis Block")

    def create_block(self, vote_data, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(time.time()),
            "vote_data": vote_data,
            "previous_hash": previous_hash,
            "hash": self.hash_block(vote_data, previous_hash)
        }
        self.chain.append(block)
        return block

    def hash_block(self, vote_data, previous_hash):
        block_string = json.dumps({"vote_data": vote_data, "previous_hash": previous_hash}, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

blockchain = Blockchain()
