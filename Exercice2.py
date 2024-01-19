from multiprocessing import Process
import os
import signal
import time
 
def greet():
    time.sleep(5)
    os.kill(os.getppid(), signal.SIGINT)
    while True :
        print("alive")

def handler(sig, frame):
    if sig == signal.SIGINT:
        os.kill(p.pid, signal.SIGKILL)

        


 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    p = Process(target=greet)
    p.start()
    p.join()