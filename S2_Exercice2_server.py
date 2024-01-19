from multiprocessing import Process, Manager
import os
import signal
import time
import sysv_ipc
    


 
if __name__ == "__main__":
    key = 128
    
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    
    running = True
    while running:
        try :
            message, t = mq.receive(block=False, type=1)
            message = str(time.asctime()).encode()
            mq.send(message, 3)
        except :
            try :
                message, t = mq.receive(block=False, type=2)
                print("the end")
                mq.remove()
                running = False
            except :
                pass
        

        
    
    