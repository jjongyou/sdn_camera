import numpy as np
import cv2
import socket
import time

# Server IP and PORT
IP = "127.0.0.1"
# IP = "10.0.0.2"
PORT = 8080

try:
    # Make TCP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))

    # Capture Camera
    # Maybe 12 is color
    # cap = cv2.VideoCapture(12, cv2.CAP_V4L2)
    # Maybe 8 is depth
    # cap = cv2.VideoCapture(8, cv2.CAP_V4L2)
    cap = cv2.VideoCapture(4, cv2.CAP_V4L2)

    while True:
        if not cap.isOpened():
            print("Not Opened")
            continue
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow('before', frame)
        flat_frame = frame.flatten()
        image_to_string = flat_frame.tobytes()

        # print("send: ",time.time())
        for i in range(20):
            start = time.time()
            sock.send(image_to_string[i*46080:(i+1)*46080])
            print("elapsed :",time.time() - start)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    cap.release()
    cv2.destroyAllWindows()
