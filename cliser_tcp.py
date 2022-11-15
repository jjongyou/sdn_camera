import numpy as np
import cv2
import socket
import time

# Server IP and PORT
# IP = "127.0.0.1"
IP = "192.168.0.4"
# IP = "10.0.0.100"
# PORT = 8321
PORT = 8080
MAX_BUF = 46080
RECV_BUF = 1024
# MAX_BUF = 1024
IMAGE_SIZE = 921600

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))
sock.listen()

try:
    cap = cv2.VideoCapture(12, cv2.CAP_V4L2)
    while True:
        server, addr = sock.accept()
        # Capture Camera
        data = server.recv(RECV_BUF)
        msg = data.decode()
        if msg == "True":
            print("msg is True")
 
        while True:
            # Make & Connect TCP Socket
            if not cap.isOpened():
                print("Not Opened")
                continue
            ret, frame = cap.read()
            if not ret:
                continue
 
            # cv2.imshow('before', frame)
            flat_frame = frame.flatten()
            image_to_string = flat_frame.tobytes()
 
            for idx in range(20):
                server.send(image_to_string[idx*46080:(idx+1)*46080])
            if idx == 19:
                break
                # server.close()
 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    # Stop streaming
    cap.release()
    cv2.destroyAllWindows()
