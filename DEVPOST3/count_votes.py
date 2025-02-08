from blockchain import Blockchain
from collections import Counter

# Load Blockchain
voting_chain = Blockchain()

# Extract votes (skip genesis block)
votes = [block['vote'] for block in voting_chain.chain if block['index'] != 1]

# Count votes using Counter
vote_counts = Counter(votes)

# Display results
print("\n📊 Voting Results will be done ✅:")
for candidate, count in vote_counts.items():
    print(f"🗳 Candidate {candidate}: {count} votes")

# Check Blockchain Integrity
if voting_chain.is_chain_valid():
    print("\n✅ Blockchain Integrity Verified: No Tampering Detected!")
else:
    print("\n⚠ WARNING: Blockchain Tampering Detected!")
