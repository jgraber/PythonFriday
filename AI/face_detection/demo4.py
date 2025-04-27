import cv2
import numpy as np
import time

start = time.time()

prototxt_file = './models/deploy.prototxt.txt'
model_file = './models/res10_300x300_ssd_iter_140000.caffemodel'
conf_min = 0.5

image = cv2.imread('people-1979261_640.jpg')
(h, w) = image.shape[:2]

network = cv2.dnn.readNetFromCaffe(prototxt_file, model_file)
blob = cv2.dnn.blobFromImage(cv2.resize(image, (900, 900)), 1.0, (900, 900), (104.0, 117.0, 123.0))
network.setInput(blob)
detections = network.forward()
faces = 0
for i in range(0, detections.shape[2]):
  confidence = detections[0, 0, i, 2]
  if confidence > conf_min:
    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
    (start_x, start_y, end_x, end_y) = box.astype("int")
    cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
    faces += 1

end = time.time()
print("Detection time: {:.2f} s".format(end - start))
print(f"Faces found: {faces}")

cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()