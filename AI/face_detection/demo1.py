# pip install opencv-python
# https://pixabay.com/photos/people-business-meeting-1979261/
import cv2
import time

start = time.time()

# Load a pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the input image
image = cv2.imread('people-1979261_640.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

end = time.time()
print("Detection time: {:.2f} s".format(end - start))
print(f"Faces found: {len(faces)}")

# Show the output
cv2.imshow('Detected Face', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

