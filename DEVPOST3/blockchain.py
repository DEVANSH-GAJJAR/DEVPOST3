import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []  # Stores all blocks
        self.pending_votes = []  # Stores unconfirmed votes

        # Create the Genesis Block (first block)
        self.create_block(voter_id="Genesis", vote="Genesis", previous_hash="0")

    def create_block(self, voter_id, vote, previous_hash):
        """Creates a new block and adds it to the blockchain."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'voter_id': voter_id,
            'vote': vote,
            'previous_hash': previous_hash,
            'hash': ""  # Will be updated after computing
        }

        # Calculate hash for the block
        block['hash'] = self.compute_hash(block)
        self.chain.append(block)
        return block

    def compute_hash(self, block):
        """Computes SHA-256 hash of a block."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    def add_vote(self, voter_id, vote):
        """Adds a new vote (block) to the blockchain."""
        last_block = self.get_last_block()
        new_block = self.create_block(voter_id, vote, last_block['hash'])
        return new_block

    def is_chain_valid(self):
        """Validates the blockchain (checks hash consistency)."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current['previous_hash'] != previous['hash']:
                return False

            if current['hash'] != self.compute_hash(current):
                return False

        return True
