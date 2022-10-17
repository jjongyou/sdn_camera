import numpy as np
import cv2
import socket
import time

# Setting
# UDP_IP = "127.0.0.1"
UDP_IP = "10.0.0.2"
UDP_PORT = 8080
MAX_BUF = 46080
# MAX_BUF = 1024
IMAGE_SIZE = 921600

# Load Yolov3
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Make UDP Socket and Bind to Client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

try:
    color_image = np.array([])
    labels = []
    while True:
        image_data = b''
        while True:
            data, addr = sock.recvfrom(MAX_BUF)
            image_data += data
            # print(len(image_data))

            if len(image_data) == IMAGE_SIZE:
                print("receive: ", time.time())
                image_frame = np.frombuffer(image_data, dtype=np.uint8)
                color_image = image_frame.reshape(480, 640, 3)
                # cv2.imshow('color_depth', color_image)
                img = cv2.resize(color_image, None, fx=0.4, fy=0.4)
                height, width, channels = img.shape
 
                # Detecting objects
                blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                start = time.time()
                outs = net.forward(output_layers)
 
                class_ids = []
                confidences = []
                boxes = []
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            # Object detected
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
 
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                for i in range(len(boxes)):
                    if i in indexes:
                        label = str(classes[class_ids[i]])
                        labels.append(label)
                print("elapsed time : ", time.time() - start)
                print("=== Detect Object ===")
                print(labels)
                print("=====================")
                labels.clear()
                break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    print("Exit")
