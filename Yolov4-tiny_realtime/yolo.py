import numpy as np
import cv2
import imutils
from math import sqrt


NMS_THRESHOLD = 0.3
MIN_CONFIDENCE = 0.2


# 參考來源: https://data-flair.training/blogs/pedestrian-detection-python-opencv/
def pedestrian_detection(image, model, layer_name, personidz=0):
    (H, W) = image.shape[:2]
    results = []

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    model.setInput(blob)
    layerOutputs = model.forward(layer_name)

    boxes = []
    centroids = []
    confidences = []

    for output in layerOutputs:
        for detection in output:

            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if classID == personidz and confidence > MIN_CONFIDENCE:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                centroids.append((centerX, centerY))
                confidences.append(float(confidence))
    idzs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)

    if len(idzs) > 0:
        for i in idzs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            res = (confidences[i], (x, y, x + w, y + h), centroids[i])
            results.append(res)
    return results


def cal_distance(results, last_result, status):
    if status and len(results) != 0:
        for i in range(len(results)):
            results[i] += (0,)
        return results
    if len(results) == len(last_result):
        for i in range(len(results)):
            distance = sqrt(
                (results[i][2][0] - last_result[i][2][0]) ** 2 + (results[i][2][1] - last_result[i][2][1]) ** 2)
            print(results[i][2][0])
            results[i] += (distance,)
    elif len(results) > len(last_result):  # 多人
        all_distance = []
        if len(last_result) == 0:
            for i in range(len(results)):
                results[i] += (10000,)
            return results
        for i in range(len(results)):
            eval_Distance = []
            for j in range(len(last_result)):
                distance = sqrt(
                    (results[i][2][0] - last_result[j][2][0]) ** 2 + (results[i][2][1] - last_result[j][2][1]) ** 2)
                eval_Distance.append(distance)
            all_distance.append(min(eval_Distance))
        max_dis = 0
        pos = 0
        for i in range(len(all_distance)):
            if all_distance[i] > max_dis:
                pos = i
                max_dis = all_distance[i]
        for i in range(len(all_distance)):
            if i == pos:
                results[i] += (10000,)
            else:
                results[i] += (all_distance[i],)

    elif len(results) < len(last_result):  # 少人
        for i in range(len(results)):
            eval_Distance = []
            for j in range(len(last_result)):
                distance = sqrt((results[i][2][0] - last_result[j][2][0]) ** 2 + (
                        results[i][2][1] - last_result[j][2][1]) ** 2)
                eval_Distance.append(distance)
            results[i] += (min(eval_Distance),)

    return results


# 讀入類別名稱
labelsPath = "coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

# 讀入yolo-v4參數以及設定檔
weights_path = "yolov4-tiny.weights"
config_path = "yolov4-tiny.cfg"
model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
layer_name = model.getLayerNames()
layer_name = [layer_name[i - 1] for i in model.getUnconnectedOutLayers()]

# 針對筆電視訊影像進行偵測，也可改為其他影像來源
cap = cv2.VideoCapture(0)

last_amount = 0
last_result = []
first_time = True
while True:
    (grabbed, image) = cap.read()

    if not grabbed:
        break

    image = imutils.resize(image)
    results = pedestrian_detection(image, model, layer_name,
                                   personidz=LABELS.index("person"))
    results = cal_distance(results, last_result, first_time)

    print(results)
    # 畫出偵測到的每個方框
    for i in range(len(results)):

        if results[i][3] > 50:
            cv2.rectangle(image, (results[i][1][0], results[i][1][1]), (results[i][1][2], results[i][1][3]),
                          (255, 255, 0), 2)
        else:
            cv2.rectangle(image, (results[i][1][0], results[i][1][1]), (results[i][1][2], results[i][1][3]),
                          (0, 255, 0), 2)

    first_time = False
    last_amount = len(results)
    last_result = results
    cv2.imshow("Detection", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
