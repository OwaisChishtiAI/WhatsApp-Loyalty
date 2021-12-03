import cv2
import numpy as np

net = cv2.dnn.readNet('model/yolov3_training_last.weights', 'model/yolov3_testing.cfg')
print("[INFO] YoLo model loaded.")
classes = []
with open("model/classes.txt", "r") as f:
    classes = f.read().splitlines()

def crop_roi_from_reciept(customer_number):
    global net, classes
    img = cv2.imread(f"uploads/{customer_number}/.jpg")
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            confidence = str(round(confidences[i],2))
        cropped_image = img[y:y+h, x:x+w]
        cv2.imwrite(f'uploads/{customer_number}/cropped.jpg', cropped_image)
        print("[INFO] ROI found, Saved cropped image.")
        return True
    else:
        print("[INFO] YoLo unable to find ROI")
        return False