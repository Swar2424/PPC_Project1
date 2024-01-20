import threading
import random
from multiprocessing import Process, Value
 
def pi_test(n, res):
    for i in range (n) :
        x = random.random()
        y = random.random()
        if x**2 + y**2 < 1 :
            res.value += 1
    
    
 
if __name__ == "__main__":
    res = Value('i', 0)
    print("Starting thread:", threading.current_thread().name)
    index = int(input("arg : "))
    thread = threading.Thread(target=pi_test, args=(index,res,))
    thread.start()
    thread.join()
    print(res.value/index*4)
    print("Ending thread:", threading.current_thread().name)