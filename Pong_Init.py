import PongConst as PConst
import multiprocessing as mp
from DaylightPong import PongGameMain
from multiprocessing import Process, Pipe, Queue, Array

if __name__ == '__main__':
    mp.set_start_method('spawn')
    Com_G_M = Array('i', range(PConst.MSG_DATA_TOTAL))
    P_PongGame = mp.Process(target=PongGameMain, args=(Com_G_M,))
    P_PongGame.start()

    while P_PongGame.is_alive():  # termiar tarea
        Com_G_M[PConst.PALETA2_KEY] = Com_G_M[PConst.PALETA1_KEY]
        Com_G_M[PConst.PALETA2_TYPE] = Com_G_M[PConst.PALETA1_TYPE]

        print(str(Com_G_M[PConst.PALETA1_KEY]) +
              "Type ----" + str(Com_G_M[PConst.PALETA1_TYPE]))

    print("Fin")
