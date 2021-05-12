import socket

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket UDP Aberto")

socketUDP.send(b'fuck you')

