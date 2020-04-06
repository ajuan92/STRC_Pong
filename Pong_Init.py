# import DaylightPong
import multiprocessing as mp
from DaylightPong import PongGameMain
from multiprocessing import Process, Pipe

if __name__ == '__main__':
    Com_G_M, Com_M_G = Pipe()
    P_PongGame = mp.Process(target=PongGameMain, args=(Com_G_M,))
    mp.set_start_method('spawn')
    P_PongGame.start()

    while P_PongGame.is_alive():  # termiar tarea
        print(Com_M_G.recv())
        print(P_PongGame.is_alive())

    print("Fin")
