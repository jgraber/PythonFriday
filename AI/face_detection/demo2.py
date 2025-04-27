# uv pip install mediapipe opencv-python


import cv2
import mediapipe as mp
import time

start = time.time()

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Read the image
image = cv2.imread('people-1979261_640.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect faces
results = face_detection.process(image_rgb)

# Draw bounding boxes
if results.detections:
    for detection in results.detections:
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

end = time.time()
print("Detection time: {:.2f} s".format(end - start))
print(f"Faces found: {len(results.detections)}")

# Show the result
cv2.imshow('MediaPipe Face Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
