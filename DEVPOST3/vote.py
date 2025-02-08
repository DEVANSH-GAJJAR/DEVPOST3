import cv2
import sqlite3
from blockchain import Blockchain
import time

# Initialize Blockchain
voting_chain = Blockchain()

# Connect to the database
conn = sqlite3.connect("voters.db")
cursor = conn.cursor()

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Cannot access the webcam.")
    exit()

# Get voter's name
voter_name = input("Enter your name to vote: ")

# Check if voter exists in the database
cursor.execute("SELECT * FROM voters WHERE name=?", (voter_name,))
voter = cursor.fetchone()

if voter is None:
    print("❌ Voter not found! Please register first.")
    exit()

print("✅ Voter found! Please look at the camera for verification.")

# Face verification loop
face_verified = False
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error capturing frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Voter Authentication - Press 'V' to Verify", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('v') and len(faces) > 0:
        print("✅ Face Verified! You may now vote.")
        face_verified = True
        break
    elif key == ord('q'):
        print("❌ Voting cancelled.")
        break

cap.release()
cv2.destroyAllWindows()

# If face verification passed, proceed to voting
if face_verified:
    vote_choice = input("Enter your vote (Candidate A/B/C): ").strip().upper()

    if vote_choice in ['A', 'B', 'C']:
        # Store vote in Blockchain
        voting_chain.add_vote(voter_name, vote_choice)
        print(f"🎉 Vote for '{vote_choice}' has been recorded in Blockchain!")
    else:
        print("❌ Invalid vote! Please vote for Candidate A, B, or C.")


#after voting 
vote_block = voting_chain.add_vote(voter_name,vote_choice)
vote_hash = vote_block['hash']     #UNiue voter id 

print(f"\n VOTING RECIPT :{vote_hash}")
print("Save this for verification. Your Vote is surely recorded!")