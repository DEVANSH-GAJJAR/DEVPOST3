from blockchain import Blockchain

# Load the blockchain
voting_chain = Blockchain()

# Display all votes
print("\n🔹 Voting Results:")
for block in voting_chain.chain:
    if block['index'] != 1:  # Ignore Genesis block
        print(f"Voter: {block['voter_id']} → Voted for: {block['vote']}")
