import sys
from Apppath import APPPATH
sys.path.insert(1, APPPATH)

import socket
import Addr_Dir
import PongConst as PConst

RevCommand = [0, 0, 0]


def Convert(string):
    li = list(string.split(" "))
    return li


def CloseServerNet(connection):
    connection.close()


def ServerNet(ProcesData):

    PORT = Addr_Dir.TCP_PORT

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (Addr_Dir.IP_PLAYER_1, PORT)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(Addr_Dir.BUFFER_SIZE)
            # print(data)
            RevCommand = Convert(data.decode('utf-8'))
            ProcesData[0] = int(RevCommand[0])
            ProcesData[1] = int(RevCommand[1])
            ProcesData[2] = int(RevCommand[2])
            ProcesData[3] = int(RevCommand[3])
            ProcesData[4] = int(RevCommand[4])
            ProcesData[5] = int(RevCommand[5])
            ProcesData[6] = int(RevCommand[6])
            ProcesData[7] = int(RevCommand[7])
            ProcesData[8] = int(RevCommand[8])
            ProcesData[9] = int(RevCommand[9])

            if data:
                connection.sendall(str.encode(RevCommand[0]))
            else:
                #print('no data from', client_address)
                break
