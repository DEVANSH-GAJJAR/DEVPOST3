import cv2
import sqlite3
import numpy as np

# Connect to SQLite database
conn = sqlite3.connect("voters.db")
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    face_image BLOB
)
""")
conn.commit()

# Load OpenCV's Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Cannot access the webcam.")
    exit()

voter_name = input("Enter voter's name: ")  # Ask for the voter's name

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Cannot read frame from webcam.")
        break

    # Convert to grayscale (better for face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the live video feed
    cv2.imshow("Register Voter - Press 'S' to Save", frame)

    # Press 's' to capture and save the face
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and len(faces) > 0:
        (x, y, w, h) = faces[0]  # Take the first detected face
        face_image = frame[y:y+h, x:x+w]  # Crop the face

        # Convert face image to binary format for database storage
        _, buffer = cv2.imencode(".jpg", face_image)
        face_blob = buffer.tobytes()

        # Insert into database
        cursor.execute("INSERT INTO voters (name, face_image) VALUES (?, ?)", (voter_name, face_blob))
        conn.commit()

        print(f"✅ Voter '{voter_name}' registered successfully!")
        break  # Exit the loop after capturing

    # Press 'q' to quit without saving
    elif key == ord('q'):
        print("❌ Registration canceled.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
conn.close()
