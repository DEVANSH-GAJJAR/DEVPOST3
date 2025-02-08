import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("voters.db")
cursor = conn.cursor()

# Fetch all voter records
cursor.execute("SELECT id, name FROM voters")
voters = cursor.fetchall()

# Display the records
print("\nRegistered Voters:")
print("==================")
for voter in voters:
    print(f"ID: {voter[0]}, Name: {voter[1]}")

conn.close()
