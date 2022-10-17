import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
request = []

print("input : start_host, end_host and bandwidth")
request = input().split(" ")

for item in request:
    sock.sendto(item.encode(), ("127.0.0.1", 8080))
    print(item.encode())
    print(type(item.encode()))
    print(len(item.encode()))
