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


SendPongMsg = [0, " ", 0, " ", 0, " ", 0,
               " ", 0, " ", 0, " ", 0, " ", 0, " ", 0, " ", 0, " ", 0, " ", 0, " ", 0]

GLOB_ErrCount = 0
GLOB_ErrState = 0

OtherPrevTime = 0

RCONECT = 5
CCONECT = 6


def MonitorLog(RecvMsg, PrevTime, ErrorState, ErrCount):

    while ErrorState[0] == 0:
        time.sleep(0.1)
        pass
        if RecvMsg[PConst.RTIME] != PrevTime:
            CurrDeltatime = RecvMsg[PConst.RTIME] - PrevTime
            PrevTime = RecvMsg[PConst.RTIME]
            if CurrDeltatime > PConst.MS_MSG_DEADLINE:
                ErrCount += 1
            else:
                ErrCount = 0

            if ErrCount >= PConst.LOST_MSG_LIMIT:
                ErrorState[0] = 1
            # Se imprime interpreta como numero negativo por el tipo de dato resivido
            print("OTHER_PLAYER_MSG: " + str(RecvMsg[PConst.RTIME]) + " DeltaTime: " + str(
                CurrDeltatime) + " ErrorCoutn: " + str(ErrCount) + " GlobalErrorState: " + str(ErrorState[0]))


def listToString(A):

    # initialize an empty string
    # return string
    return ("".join([str(a) for a in A]))


if __name__ == '__main__':
    mp.set_start_method('spawn')
    Com_G_M = Array('i', range(PConst.MSG_DATA_TOTAL))
    Com_R_M = Array('i', range(PConst.MSG_DATA_TOTAL))
    GLOB_ErrState = Array('i', range(1))
    GLOB_ErrState[0] = 0
    for index in range(PConst.MSG_DATA_TOTAL):
        Com_G_M[index] = 0
        Com_R_M[index] = 000000000

    P_RXnet = mp.Process(target=ServerNet, args=(Com_R_M,))
    P_RXnet.start()

    P_PongGame = mp.Process(target=PongGameMain, args=(Com_G_M,))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("START_SYNCRO")
    s.connect((Addr_Dir.IP_PLAYER_OTHE, Addr_Dir.TCP_PORT))

    InicialTime = time.time()

    ConectDeadLine = 0
    ConectionState = 0
    SecondConection = 0

    SendPongMsg[PConst.ESTADO_CONECCION] = 2
    SendPongMsg[PConst.CTIME] = int(1000 * time.time())
    print(SendPongMsg[PConst.CTIME])
    s.sendall(str.encode(listToString(SendPongMsg)))
    data = s.recv(Addr_Dir.BUFFER_SIZE)
    print(data)
    while ConectDeadLine < 10000:
        RecivSincro = int(data)
        print(Com_R_M[PConst.ESTADO_CONECCION])
        if Com_R_M[PConst.ESTADO_CONECCION] == 0 and ConectDeadLine <= 1:
            SecondConection = 1
            print("SEGUNDO CONECTADO")

        if (Com_R_M[PConst.ESTADO_CONECCION] == 2):

            CurrTime = time.time()
            print(str(Com_G_M[PConst.ESTADO_CONECCION]) +
                  " Tiempo de inicio delta " + str(CurrTime - InicialTime))
            time.sleep(0.30)
            if SecondConection == 0:
                if Com_R_M[PConst.ESTADO_CONECCION] == 1:
                    time.sleep(0.65)
                    CurrTime = time.time()
                    print(str(Com_G_M[PConst.ESTADO_CONECCION]) +
                          " Tiempo de inicio PRIMERO " + str(CurrTime - InicialTime))
                    print("PRIMERO LISTO")
                    OtherPrevTime = Com_R_M[PConst.RTIME]
                    #Addr_Dir.SetAsPlaye1()
                    ConectionState = 1
                    Com_G_M[PConst.ESTADO_CONECCION] = 1
                    ConectDeadLine = 10000
                    P_PongGame.start()
            else:
                Com_R_M[PConst.ESTADO_CONECCION] = 1
                SendPongMsg[PConst.ESTADO_CONECCION] = 1
                s.sendall(str.encode(listToString(SendPongMsg)))
                CurrTime = time.time()
                print(str(Com_G_M[PConst.ESTADO_CONECCION]) +
                      " Tiempo de inicio SEGUNDO " + str(CurrTime - InicialTime))
                print("SEGUNDO LISTO")
                OtherPrevTime = Com_R_M[PConst.RTIME]
                #Addr_Dir.SetAsPlaye2()
                ConectionState = 1
                Com_G_M[PConst.ESTADO_CONECCION] = 1
                ConectDeadLine = 10000
                P_PongGame.start()

        time.sleep(0.010)
        ConectDeadLine = ConectDeadLine + 1
    TestDelay = 0.001
    if ConectionState == 1:
        P_Monitor = mp.Process(target=MonitorLog, args=(
            Com_R_M, OtherPrevTime, GLOB_ErrState, GLOB_ErrCount,))
        P_Monitor.start()

        while P_PongGame.is_alive():

            Com_G_M[PConst.GLOBAL_ERR_ST] = GLOB_ErrState[0]

            if Addr_Dir.ID_CURRENT_PLAYER == Addr_Dir.PLAYER_1_ID:
                SendPongMsg[PConst.CKEY] = Com_G_M[PConst.PALETA1_KEY]
                SendPongMsg[PConst.CTYPE] = Com_G_M[PConst.PALETA1_TYPE]

                SendPongMsg[PConst.CPX] = Com_G_M[PConst.BALL_P_X]
                SendPongMsg[PConst.CPY] = Com_G_M[PConst.BALL_P_Y]
                SendPongMsg[PConst.CVX] = Com_G_M[PConst.BALL_V_X]
                SendPongMsg[PConst.CVY] = Com_G_M[PConst.BALL_V_Y]

                SendPongMsg[PConst.CSCOREP1] = Com_G_M[PConst.SCORE_PLAYER_1]
                SendPongMsg[PConst.CSCOREP2] = Com_G_M[PConst.SCORE_PLAYER_2]

            else:
                SendPongMsg[PConst.CKEY] = Com_G_M[PConst.PALETA2_KEY]
                SendPongMsg[PConst.CTYPE] = Com_G_M[PConst.PALETA2_TYPE]

            SendPongMsg[PConst.CTIME] = int(1000 * time.time())

            if P_RXnet.is_alive():
                s.sendall(str.encode(listToString(SendPongMsg)))
                try:
                    data = s.recv(Addr_Dir.BUFFER_SIZE)
                except ValueError:
                    Com_G_M[PConst.ESTADO_CONECCION] = 0
                    Com_G_M[PConst.GLOBAL_ERR_ST] = 1

            if Addr_Dir.ID_OTHE_PLAYER == Addr_Dir.PLAYER_2_ID:
                Com_G_M[PConst.PALETA2_KEY] = Com_R_M[PConst.RKEY]
                Com_G_M[PConst.PALETA2_TYPE] = Com_R_M[PConst.RTYPE]
            else:
                Com_G_M[PConst.PALETA1_KEY] = Com_R_M[PConst.RKEY]
                Com_G_M[PConst.PALETA1_TYPE] = Com_R_M[PConst.RTYPE]

                Com_G_M[PConst.BALL_P_Y] = Com_R_M[PConst.RPY]
                Com_G_M[PConst.BALL_V_X] = Com_R_M[PConst.RVX]
                Com_G_M[PConst.BALL_V_Y] = Com_R_M[PConst.RPX]

                Com_G_M[PConst.SCORE_PLAYER_1] = Com_R_M[PConst.RSCOREP1]
                Com_G_M[PConst.SCORE_PLAYER_2] = Com_R_M[PConst.RSCOREP2]

                Com_G_M[PConst.BALL_P_X] = Com_R_M[PConst.RPX]
            # Prueba para validad DEADLINE, ELMININAR PARA FUNCIONAMIENTO NORMAL
            if Com_G_M[PConst.SCORE_PLAYER_1] > 5:
                time.sleep(TestDelay)
                TestDelay = TestDelay + 0.001

            # print(TestDelay)
            #print(Com_R_M[PConst.RTIME]  + 2**32)
            # print(time.time())
            # print(SendPongMsg[PConst.CTIME])

    P_Monitor.terminate()
    P_PongGame.terminate()
    P_RXnet.terminate()
    s.close()
    print("Fin")
