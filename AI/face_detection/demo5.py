import cv2
import dlib
import time

start = time.time()

image = cv2.imread('people-1979261_640.jpg')
cnn_detector = dlib.cnn_face_detection_model_v1('./models/mmod_human_face_detector.dat')
detections = cnn_detector(image, 2)
for face in detections:
  l, t, r, b, c = face.rect.left(), face.rect.top(), face.rect.right(), face.rect.bottom(), face.confidence
  cv2.rectangle(image, (l, t), (r, b), (0, 0, 255), 2)

end = time.time()
print("Detection time: {:.2f} s".format(end - start))
print(f"Faces found: {len(detections)}")

cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()