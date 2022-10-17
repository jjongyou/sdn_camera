import pyrealsense2 as rs
import numpy as np
import cv2

# Load Yolov3
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

# device is Intel RealSense D435 (S/N: 213622070558  FW: 05.12.07.150
# device = pipeline_profile.get_device()

# device_product_line is D400
# device_product_line = str(device.get_info(rs.camera_info.product_line))

# Depth Camera Configuration
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Color Camera Configuration
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        # cv2.imshow('color_depth', color_image)
        # print("h, w : ", color_frame.height, color_frame.width)

        # Read Image Frame
        # img = cv2.imread(color_image)
        # img = cv2.resize(img, None, fx=0.4, fy=0.4)
        img = cv2.resize(color_image, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
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
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        cv2.imshow("Image", img)

        # print(type(color_image))
        # print(len(color_image))
        # print(type(color_image.tobytes()))
        # print(len(color_image.tobytes()))

        cv2.waitKey(1)

finally:
    # Stop streaming
    pipeline.stop()
