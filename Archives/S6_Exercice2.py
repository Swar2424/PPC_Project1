from multiprocessing import Process, Array, Semaphore, Value
    
    
def fibonacci(n, arr, write_l, read_l, end):
    read_l.acquire()
    arr[0] = 0
    write_l.release()

    read_l.acquire()
    arr[1] = 1

    for i in range(2,n):
        write_l.release()
        read_l.acquire()
        arr[i%5] = arr[i%5-1] + arr[i%5-2]

    end.value = 1
    write_l.release()


def reader(arr, write_l, read_l, end) :
    i=0
    while end.value == 0 :
        write_l.acquire()
        print(arr[i%5])
        i+=1
        read_l.release()

 
if __name__ == "__main__":
    n = int(input("Fibo : "))
    arr = Array('i', range(5))
    end = Value('i', 0)
    write_l = Semaphore(0)
    read_l = Semaphore(1)

    w = Process(target=fibonacci, args =(n, arr, write_l, read_l, end))
    r = Process(target=reader, args =(arr, write_l, read_l, end))

    w.start()
    r.start()
    w.join()
    r.join()

