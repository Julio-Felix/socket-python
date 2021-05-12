import socket
import numpy as np  # pip install numpy


socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
transmissor = ("127.0.0.1", 2020)
receptor = ("127.0.0.1", 3030)
socketUDP.bind(transmissor)
buff_size = 10000

next_sequence_number = 0


def calculate_checksum(data):
    data_sum = np.uint16(0)
    for element in data:
        data_sum += element
    return np.invert(data_sum)


def verify_checksum(data):
    data_sum = np.uint16(0)
    for element in data:
        data_sum += element
    return data_sum == 0xFFFF


def udt_send(packet):
    socketUDP.sendto(packet.tobytes(), receptor)


def rdt_rcv():
    while True:
        message, source = socketUDP.recvfrom(buff_size)
        if source == receptor:
            return np.frombuffer(message, dtype=np.uint16)


def rdt_send(data):
    global next_sequence_number

    sndpkt = np.array([], np.uint16)
    sndpkt = np.append(sndpkt, np.uint16(next_sequence_number))
    sndpkt = np.append(sndpkt, np.uint16(0))  # checksum
    sndpkt = np.concatenate((sndpkt, data))

    sndpkt[1] = calculate_checksum(sndpkt)
    udt_send(sndpkt)

    while True:
        rcvpkt = rdt_rcv()
        is_corrupt = not verify_checksum(rcvpkt)
        is_ack = rcvpkt[2] == True
        is_nack = rcvpkt[2] == False
        print("Dados recebidos ", rcvpkt)
        print("Está corrompido? ", is_corrupt)
        print("Está Nack? ", is_nack)
        print("Está Ack? ", is_ack)
        print("Seq Num? ", next_sequence_number)
        
        if is_corrupt or is_nack:
            udt_send(sndpkt)
        if is_ack and not is_corrupt:
            break

    if next_sequence_number == 0:
        next_sequence_number = 1
    else:
        next_sequence_number = 0


if __name__ == "__main__":
    i = 1
    while i <= 3:
        dados = np.random.randint(5, size=10, dtype=np.uint16)
        print(f'Dados a serem enviados {dados}')
        rdt_send(dados)
        i+=1
