import numpy as np
import cv2
import socket
import time

# Setting
IP = "127.0.0.1"
# IP = "192.168.0.2"
# IP = "0.0.0.0"
# PORT = 8321
PORT = 8080
MAX_BUF = 46080
# MAX_BUF = 1024
IMAGE_SIZE = 921600

# Make UDP Socket and Bind to Client
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))
sock.listen()

try:
    server, addr = sock.accept()
    print("[CONNECT] ", addr[0],":",addr[1])
    while True:
        image_data = b''
        start = time.time()
        step = MAX_BUF
        while True:
       
            data = server.recv(step)
            if not data:
                print("No Data: from " + addr[0],":",addr[1])
                break
            image_data += data
            # print(len(image_data))
            # print(type(image_data))

            if len(image_data) == IMAGE_SIZE:
                print("image received :", time.time() - start)
                image_frame = np.frombuffer(image_data, dtype=np.uint8)
                color_image = image_frame.reshape(480, 640, 3)
                cv2.imshow('after', color_image)
                break
            elif len(image_data) < IMAGE_SIZE:
                step = IMAGE_SIZE - len(image_data)
                if step > MAX_BUF:
                    step = MAX_BUF
            elif len(image_data) > IMAGE_SIZE:
                print("[ERROR] Size is big")
                break



        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    sock.close()
    print("Exit")
