import numpy as np
import cv2
import socket
import time

# Setting
# RECV_IP = "127.0.0.1"
SDN_IP = "10.0.0.100"
SSH_IP = "192.168.0.7"
SDN_PORT = 8080
SSH_PORT = 8321
MAX_BUF = 46080
RECV_BUF = 1024
IMAGE_SIZE = 921600

# Make & Bind to SDN_Client (Odroid)
sdn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sdn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sdn_sock.bind((SDN_IP, SDN_PORT))
sdn_sock.listen()

# Make & Bind to SSH_Client (Desktop)
ssh_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssh_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ssh_sock.bind((SSH_IP, SSH_PORT))
ssh_sock.listen()


try:
    sdn_server, sdn_addr = sdn_sock.accept()
    print("[CONNECT] ", sdn_addr[0],":",sdn_addr[1])
    ssh_server, ssh_addr = ssh_sock.accept()
    print("[CONNECT] ", ssh_addr[0],":",ssh_addr[1])
    while True:
        start = time.time()
        image_data = b''
        step = MAX_BUF
        while True:
       
            sdn_data = sdn_server.recv(step)
            if not sdn_data:
                print("No Data: " + addr[0],":",addr[1])
                break
            image_data += sdn_data
            ssh_server.send(sdn_data)

            if len(image_data) == IMAGE_SIZE:
                print("image received :", time.time() - start)
                break
            elif len(image_data) < IMAGE_SIZE:
                step = IMAGE_SIZE - len(image_data)
                if step > MAX_BUF:
                    step = MAX_BUF
            elif len(image_data) > IMAGE_SIZE:
                print("[BIG]", len(image_data))
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    sdn_sock.close()
    ssh_sock.close()
    print("Exit")
