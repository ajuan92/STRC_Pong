import time

import Addr_Dir
import PongConst as PConst
import multiprocessing as mp

import socket
import Addr_Dir

from Red_Server import ServerNet
from DaylightPong import PongGameMain
from multiprocessing import Process, Array


SendPongMsg = [0, " ", 0, " ", 0]



def listToString(A):

    # initialize an empty string
    # return string
    return ("".join([str(a) for a in A]))


if __name__ == '__main__':
    mp.set_start_method('spawn')
    Com_G_M = Array('i', range(PConst.MSG_DATA_TOTAL))
    Com_R_M = Array('i', range(PConst.MSG_DATA_TOTAL))
    P_PongGame = mp.Process(target=PongGameMain, args=(Com_G_M,))
    P_PongGame.start()

    P_RXnet = mp.Process(target=ServerNet, args=(Com_R_M,))
    P_RXnet.start()

    time.sleep(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((PConst.IP_PLAYER_1, Addr_Dir.TCP_PORT))

    while P_PongGame.is_alive():  # termiar tarea

        SendPongMsg[PConst.CKEY] = Com_G_M[PConst.PALETA1_KEY]
        SendPongMsg[PConst.CTYPE] = Com_G_M[PConst.PALETA1_TYPE]
        SendPongMsg[PConst.CTIME] = 5  # time.time()

        if P_RXnet.is_alive():
            s.sendall(str.encode(listToString(SendPongMsg)))
            data = s.recv(Addr_Dir.BUFFER_SIZE)

        Com_G_M[PConst.PALETA2_KEY] = Com_R_M[PConst.RKEY]
        Com_G_M[PConst.PALETA2_TYPE] = Com_R_M[PConst.RTYPE]

        print("KEY:  " + str(Com_G_M[PConst.PALETA1_KEY])  + " " + str(Com_G_M[PConst.PALETA2_KEY]))
        print("TYPE: " + str(Com_G_M[PConst.PALETA1_TYPE])  + " " + str(Com_G_M[PConst.PALETA2_TYPE]))

    P_RXnet.terminate()
    s.close()
    print("Fin")
