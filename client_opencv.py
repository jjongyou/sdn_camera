import numpy as np
import cv2
import socket
import time

# Server IP and PORT
# UDP_IP = "127.0.0.1"
UDP_IP = "10.0.0.2"
UDP_PORT = 8080

try:
    # Make UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Capture Camera
    # Maybe 12 is color
    cap = cv2.VideoCapture(12, cv2.CAP_V4L2)
    # Maybe 8 is depth
    # cap = cv2.VideoCapture(8, cv2.CAP_V4L2)

    while True:
        if not cap.isOpened():
            print("Not Opened")
            continue
        ret, frame = cap.read()
        if not ret:
            continue

        flat_frame = frame.flatten()
        image_to_string = flat_frame.tobytes()

        print("send: ",time.time())
        for i in range(20):
            sock.sendto(image_to_string[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    cap.release()
    cv2.destroyAllWindows()
