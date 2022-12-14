import numpy as np
import cv2
import socket
import time

# Server IP and PORT
# IP = "127.0.0.1"
# IP = "192.168.0.2"
IP = "10.0.0.100"
PORT = 8080

try:
    cap = cv2.VideoCapture(12, cv2.CAP_V4L2)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))

    while True:
        if not cap.isOpened():
            print("Not Opened")
            continue
        ret, frame = cap.read()
        if not ret:
            continue

        # cv2.imshow('before', frame)
        flat_frame = frame.flatten()
        image_to_string = flat_frame.tobytes()

        sock.sendall(image_to_string)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    cap.release()
    cv2.destroyAllWindows()
