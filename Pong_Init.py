# import DaylightPong
import multiprocessing as mp
from DaylightPong import PongGameMain
from multiprocessing import Process, Pipe, Queue, Array

if __name__ == '__main__':
    mp.set_start_method('spawn')
    Com_G_M = Array('i', range(1))
    P_PongGame = mp.Process(target=PongGameMain, args=(Com_G_M,))
    P_PongGame.start()

    while P_PongGame.is_alive():  # termiar tarea
        print(Com_G_M[0])
        print("---")
        print(P_PongGame.is_alive())

    print("Fin")
