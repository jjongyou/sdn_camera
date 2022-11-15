import numpy as np
import socket
import time

# Setting
SDN_IP_TO = "10.0.0.100"
SDN_IP_FROM = "10.0.0.102"
SDN_PORT_TO = 8080
SDN_PORT_FROM = 8080
MAX_BUF = 46080
RECV_BUF = 1024
IMAGE_SIZE = 921600

# Make & Bind to SDN_Server (From Odroid)
from_sdn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
from_sdn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
from_sdn_sock.bind((SDN_IP_FROM, SDN_PORT_FROM))
from_sdn_sock.listen()

# Make & Bind to SDN_Client (To Odroid)
to_sdn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    sdn_server, sdn_addr = from_sdn_sock.accept()
    print("[CONNECT] ", sdn_addr[0],":",sdn_addr[1])
    to_sdn_sock.connect((SDN_IP_TO, SDN_PORT_TO))
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
            to_sdn_sock.send(sdn_data)

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
    from_sdn_sock.close()
    to_sdn_sock.close()
    print("Exit")
