# winget install cmake
# uv pip install face_recognition opencv-python
# pip install git+https://github.com/ageitgey/face_recognition_models

import face_recognition
import cv2
import time

start = time.time()

# Load the image
image = cv2.imread('people-1979261_640.jpg')
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Find all face locations
face_locations = face_recognition.face_locations(rgb_image)

# Draw rectangles
for top, right, bottom, left in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

end = time.time()
print("Detection time: {:.2f} s".format(end - start))
print(f"Faces found: {len(face_locations)}")

# Show the result
cv2.imshow('face_recognition Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
