import pyrealsense2 as rs
import numpy as np
import cv2
import socket
import threading

def sendImage():
    print(len(imageq))
    if imageq:
        print(len(imageq))
        color_frame = imageq.pop(0)
        color_image = np.asanyarray(color_frame.get_data())
        # cv2.imshow('color_depth', color_image)
        flat_image = color_image.flatten()
        # image_to_string = flat_image.tostring()
        image_to_string = flat_image.tobytes()
        # print(len(image_to_string))
        for i in range(20):
            sock.sendto(image_to_string[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))
        # for i in range(900):
        #     sock.sendto(image_to_string[i*1024:(i+1)*1024], (UDP_IP, UDP_PORT))
  

# Server IP and PORT
UDP_IP = "127.0.0.1"
UDP_PORT = 8080

# Make UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Make Shared List
imageq = []

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

# Make Transmit Thread
# tx_thread = threading.Thread(target=sendImage)

try:
    # tx_thread.start()
    while True:
        # Wait for a coherent pair of frames: color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # imageq.append(color_frame)
        # print(len(imageq))

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow('color_depth', color_image)
        # print(type(color_image))
        # print(len(color_image))
        # print(type(color_image.tobytes()))
        # print(len(color_image.tobytes()))
        flat_image = color_image.flatten()
        # image_to_string = flat_image.tostring()
        image_to_string = flat_image.tobytes()
        # print(len(image_to_string))
        for i in range(20):
            sock.sendto(image_to_string[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))
        # for i in range(900):
        #     sock.sendto(image_to_string[i*1024:(i+1)*1024], (UDP_IP, UDP_PORT))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
