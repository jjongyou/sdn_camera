import numpy as np
import cv2
import socket
import time

# Server IP and PORT
IP = "127.0.0.1"
# IP = "10.0.0.100"
PORT = 8080

try:
    # Capture Camera
    # 12 is color on Odroid
    # cap = cv2.VideoCapture(12, cv2.CAP_V4L2)
    # 8 is depth on Odroid
    # cap = cv2.VideoCapture(8, cv2.CAP_V4L2)
    # 4 is color on Desktop
    cap = cv2.VideoCapture(4, cv2.CAP_V4L2)

    while True:
        # Make & Connect TCP Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        if not cap.isOpened():
            print("Not Opened")
            continue
        ret, frame = cap.read()
        if not ret:
            continue

        # cv2.imshow('before', frame)
        flat_frame = frame.flatten()
        image_to_string = flat_frame.tobytes()

        for i in range(20):
            sock.send(image_to_string[i*46080:(i+1)*46080])
            if i == 19:
                sock.close()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    cap.release()
    cv2.destroyAllWindows()
