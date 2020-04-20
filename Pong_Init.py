import sys
from Apppath import APPPATH
sys.path.insert(1, APPPATH)

import time
import Addr_Dir
import PongConst as PConst
import multiprocessing as mp

import socket

from Red_Server import ServerNet
from DaylightPong import PongGameMain
from multiprocessing import Process, Array


SendPongMsg = [0, " ", 0, " ", 0, " ", 0]

RCONECT = 5
CCONECT = 6


def listToString(A):

    # initialize an empty string
    # return string
    return ("".join([str(a) for a in A]))


if __name__ == '__main__':
    mp.set_start_method('spawn')
    Com_G_M = Array('i', range(PConst.MSG_DATA_TOTAL))
    Com_R_M = Array('i', range(PConst.MSG_DATA_TOTAL))

    P_RXnet = mp.Process(target=ServerNet, args=(Com_R_M,))
    P_RXnet.start()

    P_PongGame = mp.Process(target=PongGameMain, args=(Com_G_M,))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("START_SYNCRO")
    s.connect((PConst.IP_PLAYER_OTHE, Addr_Dir.TCP_PORT))

    InicialTime = time.time()

    ConectDeadLine = 0
    ConectionState = 0
    SecondConection = 0

    SendPongMsg[0] = 2
    s.sendall(str.encode(listToString(SendPongMsg)))
    data = s.recv(Addr_Dir.BUFFER_SIZE)
    print(data)
    while ConectDeadLine < 10000:
        RecivSincro = int(data)
        print(Com_R_M[0])
        if Com_R_M[0] == 0 and ConectDeadLine <= 1:
            SecondConection = 1
            print("SEGUNDO CONECTADO")

        if (Com_R_M[0] == 2):

            CurrTime = time.time()
            print(str(Com_G_M[PConst.ESTADO_CONECCION]) +
                  " Tiempo de inicio delta " + str(CurrTime - InicialTime))
            time.sleep(0.30)
            if SecondConection == 0:
                if Com_R_M[0] == 1:
                    time.sleep(0.65)
                    CurrTime = time.time()
                    print(str(Com_G_M[PConst.ESTADO_CONECCION]) +
                      " Tiempo de inicio PRIMERO " + str(CurrTime - InicialTime))
                    print("PRIMERO LISTO")
                    ConectionState = 1
                    Com_G_M[PConst.ESTADO_CONECCION] = 1
                    ConectDeadLine = 10000
                    P_PongGame.start()
            else:
                Com_R_M[0] = 1
                SendPongMsg[0] = 1
                s.sendall(str.encode(listToString(SendPongMsg)))
                CurrTime = time.time()
                print(str(Com_G_M[PConst.ESTADO_CONECCION]) +
                      " Tiempo de inicio SEGUNDO " + str(CurrTime - InicialTime))
                print("SEGUNDO LISTO")
                ConectionState = 1
                Com_G_M[PConst.ESTADO_CONECCION] = 1
                ConectDeadLine = 10000
                P_PongGame.start()

        time.sleep(0.010)
        ConectDeadLine = ConectDeadLine + 1

    if ConectionState == 1:

        while P_PongGame.is_alive():  # termiar tarea
            if Com_G_M[PConst.ESTADO_CONECCION] != 1:
                break

            if PConst.ID_CURRENT_PLAYER == PConst.PLAYER_1_ID:
                SendPongMsg[PConst.CKEY] = Com_G_M[PConst.PALETA1_KEY]
                SendPongMsg[PConst.CTYPE] = Com_G_M[PConst.PALETA1_TYPE]
            else:
                SendPongMsg[PConst.CKEY] = Com_G_M[PConst.PALETA2_KEY]
                SendPongMsg[PConst.CTYPE] = Com_G_M[PConst.PALETA2_TYPE]

            if P_RXnet.is_alive():
                s.sendall(str.encode(listToString(SendPongMsg)))
                try:
                    data = s.recv(Addr_Dir.BUFFER_SIZE)
                except ValueError:
                    Com_G_M[PConst.ESTADO_CONECCION] = 0

            if PConst.ID_OTHE_PLAYER == PConst.PLAYER_2_ID:
                Com_G_M[PConst.PALETA2_KEY] = Com_R_M[PConst.RKEY]
                Com_G_M[PConst.PALETA2_TYPE] = Com_R_M[PConst.RTYPE]
            else:
                Com_G_M[PConst.PALETA1_KEY] = Com_R_M[PConst.RKEY]
                Com_G_M[PConst.PALETA1_TYPE] = Com_R_M[PConst.RTYPE]

            # print("KEY:  " + str(Com_G_M[PConst.PALETA1_KEY]
            #                     ) + " " + str(Com_G_M[PConst.PALETA2_KEY]))
            # print("TYPE: " + str(Com_G_M[PConst.PALETA1_TYPE]
            #                     ) + " " + str(Com_G_M[PConst.PALETA2_TYPE]))

    P_RXnet.terminate()
    s.close()
    print("Fin")
