from Apppath import APPPATH
sys.path.insert(1, APPPATH)

import socket
import Addr_Dir
import PongConst as PConst



def SendMsg(Dest,Msg):
    
    # print(Dest)
    s.sendall(str.encode(Msg))
    data = s.recv(Addr_Dir.BUFFER_SIZE)

    #
