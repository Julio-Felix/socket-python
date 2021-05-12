import socket
import numpy as np  # pip install numpy

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
transmissor = ("127.0.0.1", 2020)
receptor = ("127.0.0.1", 3030)
socketUDP.bind(receptor)
buff_size = 10000

next_sequence_number = 0

def verify_checksum(data):
    data_sum = np.uint16(0)
    for element in data:
        data_sum += element
    return data_sum == 0xFFFF

def calculate_checksum(data):
    data_sum = np.uint16(0)
    for element in data:
        data_sum += element
    return np.invert(data_sum)

def udt_send(packet):
    socketUDP.sendto(packet.tobytes(), transmissor)

def rdt_rcv():
    while True:
        message, source = socketUDP.recvfrom(buff_size)
        if source == transmissor:
            return np.frombuffer(message, dtype=np.uint16)

def make_pkt(Is_ACK,seq_num):
    sndpkt = np.array([], np.uint16)
    sndpkt = np.append(sndpkt, np.uint16(seq_num))
    sndpkt = np.append(sndpkt, np.uint16(0))  # checksum
    sndpkt = np.append(sndpkt, np.uint16(Is_ACK))  # is_ack

    sndpkt[1] = calculate_checksum(sndpkt)
    return sndpkt

if __name__ == "__main__":
    
    while True:
        sndpkt = []
        print("Waiting for Data...")
        rcvpkt = rdt_rcv()
        
        notcorrupt = verify_checksum(rcvpkt)
        haseq = rcvpkt[0] == next_sequence_number
        # print(f'Dados recebidos {rcvpkt}') 
        print("Não Está Corrompido?",notcorrupt)  
        print("Tem seq?",haseq)  
        if haseq:
            if notcorrupt:
                sndpkt = make_pkt(1,next_sequence_number)
                if next_sequence_number == 0:
                    next_sequence_number = 1
                else:
                    next_sequence_number = 0
                print(f'Dados recebidos {rcvpkt}')        
            else:
                sndpkt = make_pkt(0,next_sequence_number)
        if len(sndpkt) > 0:
            print("Dados Enviados ",sndpkt)
            udt_send(sndpkt)





