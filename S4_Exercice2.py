import threading
from queue import Queue
from statistics import mean, median, stdev
import random
 
def worker(queue, data_ready):
    print("Starting thread:", threading.current_thread().name)

    data_ready.wait()
    func, data = queue.get()
    queue.task_done()
    print("done")

    while data_ready.is_set() :
        pass

    queue.put(f"{func.__name__} : {func(data)}")
    print("Ending thread:", threading.current_thread().name)
    
 
if __name__ == "__main__":   
    print("Starting thread:", threading.current_thread().name)
 
    queue = Queue()
    data_ready = threading.Event()

    ops = [min, max, mean, median, stdev]

    for i in range(len(ops)) :
        thread = threading.Thread(target=worker, args=(queue, data_ready))
        thread.start()
    
    data = [random.randint(0,500) for i in range(5000)]

    """
    data = []
    input_str = str(input("number : ")).split()
    for s in input_str:
        try:
            x = float(s)
        except ValueError:
            print("bad number", s)
        else:
            data.append(x) 
    """

    for op in ops :
        queue.put((op, data))

    data_ready.set()
    queue.join()
    data_ready.clear()

    rep = []
    for i in range(5) :
        rep.append(queue.get())

    thread.join()
    print(rep)
 
    print("Ending thread:", threading.current_thread().name)