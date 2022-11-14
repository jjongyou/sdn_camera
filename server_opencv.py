import numpy as np
import cv2
import socket

# Setting
UDP_IP = "127.0.0.1"
UDP_PORT = 8080
MAX_BUF = 46080
# MAX_BUF = 1024
IMAGE_SIZE = 921600

# Make UDP Socket and Bind to Client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

try:
    while True:
        image_data = b''
        while True:
            data, addr = sock.recvfrom(MAX_BUF)
            image_data += data
            # print(len(image_data))

            if len(image_data) == IMAGE_SIZE:
                image_frame = np.frombuffer(image_data, dtype=np.uint8)
                color_image = image_frame.reshape(480, 640, 3)
                cv2.imshow('color_depth', color_image)
                print(type(color_image))
 
                break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    print("Exit")
