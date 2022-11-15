import numpy as np
import cv2
import socket
import time

# Setting
# RECV_IP = "127.0.0.1"
SDN_IP = "10.0.0.100"
SSH_IP = "192.168.0.7"
PORT = 8080
PORT = 8080
MAX_BUF = 46080
RECV_BUF = 1024
IMAGE_SIZE = 921600

# Make & Bind to SDN_Client (Odroid)
sdn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sdn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sdn_sock.bind((SDN_IP, PORT))
sdn_sock.listen()

# Make & Bind to SSH_Client (Desktop)
ssh_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssh_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ssh_sock.bind((SSH_IP, PORT))
ssh_sock.listen()

try:
    while True:
        image_data = b''
        sdn_server, sdn_addr = sdn_sock.accept()
        print("[CONNECT] ", sdn_addr[0],":",sdn_addr[1])
        ssh_server, ssh_addr = ssh_sock.accept()
        print("[CONNECT] ", ssh_addr[0],":",ssh_addr[1])
        start = time.time()
        while True:
       
            sdn_data = sdn_server.recv(MAX_BUF)
            if not sdn_data:
                print("Disconnected by " + sdn_addr[0],":",sdn_addr[1])
                break
            image_data += sdn_data

            print(len(image_data))
            print(type(image_data))

            ssh_server.send(sdn_data)

            if len(image_data) == IMAGE_SIZE:
                print("[SDN] image received :", time.time() - start)
                image_frame = np.frombuffer(image_data, dtype=np.uint8)
                color_image = image_frame.reshape(480, 640, 3)
                image_data = b''
                start = time.time()
                # break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    sdn_sock.close()
    ssh_sock.close()
    print("Exit")
