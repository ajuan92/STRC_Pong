import socketserver
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
    server_address = (PConst.IP_PLAYER_1, PORT)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(Addr_Dir.BUFFER_SIZE)
            RevCommand = Convert(data.decode('utf-8'))
            ProcesData[0] = 0  # int(RevCommand[0])
            ProcesData[1] = int(RevCommand[1])
            ProcesData[2] = int(RevCommand[2])
            if data:
                connection.sendall(data)
            else:
                #print('no data from', client_address)
                break
