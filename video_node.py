import numpy as np
import cv2
import socket
import time

# Setting
IP = "192.168.0.7"
PORT = 8321
MAX_BUF = 46080
IMAGE_SIZE = 921600

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((IP, PORT))
    except ConnectionRefusedError as e:
        print("[ERROR] ", e)

    while True:
        image_data = b''
        step = MAX_BUF
        start = time.time()

        while True:       
            data = sock.recv(step)
            if not data:
                print("No Data: ", IP, ":", PORT)
                break
            image_data += data
            # print(len(image_data))
            # print(type(image_data))

            if len(image_data) == IMAGE_SIZE:
                print("[SDN] image received :", time.time() - start)
                start = time.time()

                image_frame = np.frombuffer(image_data, dtype=np.uint8)
                color_image = image_frame.reshape(480, 640, 3)
                cv2.imshow('desktop', color_image)
                break
            elif len(image_data) < IMAGE_SIZE:
                step = IMAGE_SIZE - len(image_data)
                if step > MAX_BUF:
                    step = MAX_BUF


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    sock.close()
    print("Exit")
