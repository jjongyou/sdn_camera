import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 8080))
request = []
recv_byte = 100
success = 3

while True:
  data, addr = sock.recvfrom(recv_byte)
  request.append(data.decode())
  if len(request) == success:
    print(request)
