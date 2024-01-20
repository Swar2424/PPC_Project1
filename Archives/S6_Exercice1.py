import threading
import random
from multiprocessing import Process, Value
 
def pi_test(n, res):
    for i in range (n) :
        x = random.random()
        y = random.random()
        if x**2 + y**2 < 1 :
            res.get_lock().acquire()
            res.value += 1
            res.get_lock().release()
    
    
 
if __name__ == "__main__":
    print("Starting thread:", threading.current_thread().name)
    res = Value('i', 0)

    numb_threads = int(input("numb_threads : "))
    index = int(input("index : "))

    for i in range (numb_threads) :
        thread = threading.Thread(target=pi_test, args=(index,res,))
        thread.start()

    thread.join()
    print(res.value/(index*numb_threads)*4)
    print("Ending thread:", threading.current_thread().name)