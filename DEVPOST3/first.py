import cv2

# Load OpenCV's Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open the webcam (0 for default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Cannot access the webcam.")
    exit()

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    if not ret:
        print("❌ Error: Cannot read frame from webcam.")
        break

    # Convert to grayscale (Haar cascades work better on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the live video with face detection
    cv2.imshow("Live Face Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
