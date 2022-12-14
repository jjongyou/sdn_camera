import numpy as np
import cv2
import socket
import time

# Setting
IP = "127.0.0.1"
# IP = "192.168.0.2"
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
    while True:
        image_data = b''
        server, addr = sock.accept()
        start = 0
        while True:
       
            data = server.recv(MAX_BUF)
            if not data:
                print("Disconnected by " + addr[0],":",addr[1])
                break
            image_data += data
            # print(len(image_data))
            # print(type(image_data))
            # if len(image_data) > IMAGE_SIZE:
            #     num = input()

            if len(image_data) == IMAGE_SIZE:
                print("elapsed :",time.time() - start)
                image_frame = np.frombuffer(image_data, dtype=np.uint8)
                color_image = image_frame.reshape(480, 640, 3)
                cv2.imshow('after', color_image)
                print(type(color_image))
                print(color_image.shape)
                print(len(image_data))
                image_data = b''
                start = time.time()
                # server.close()
                # num = input()
                # img = cv2.resize(color_image, None, fx=0.4, fy=0.4)

                # cv2.imshow("Image", img)

                # print(type(color_image))
                # print(len(color_image))
                # cv2.waitKey(1)
                # num = input()
                # break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    sock.close()
    print("Exit")
