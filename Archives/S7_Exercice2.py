from multiprocessing import Semaphore, Value, Lock
import time
import random
import threading

 
def philosopher(i, end):
    while end.value :
        think()

        mutex.acquire()

        state[i] = State.HUNGRY
        
        if (state[(i + N - 1) % N] != State.EATING) and (state[(i + 1) % N] != State.EATING):
            state[i] = State.EATING
            sem[i].release()
        
        mutex.release()

        sem[i].acquire()    
        eat(i)

        mutex.acquire()

        state[i] = State.THINKING

        if state[(i + N - 1) % N] == State.HUNGRY and  state[(i + N - 2) % N] != State.EATING:
            state[(i + N - 1) % N] = State.EATING
            sem[(i + N - 1) % N].release()

        if state[(i + 1) % N] == State.HUNGRY and state[(i + 2) % N] != State.EATING :
            state[(i + 1) % N] = State.EATING
            sem[(i + 1) % N].release()

        mutex.release()
        
        

class State:
    THINKING = 1
    HUNGRY = 2
    EATING = 3
 

def think() :
    time.sleep(random.random()/10)


def eat(i) :
    print(f"{i} is eating")

    time.sleep(random.random()/10)
    mutex2.acquire()
    ate[i] += 1
    mutex2.release()

    print(f"{i} has stopped")


if __name__ == "__main__":
    N = 5
    end = Value('i', 1)
    state = [State() for i in range(N)]
    sem = [Semaphore(0) for i in range(N)]
    ate = [0 for i in range (N)]
    mutex = Lock()
    mutex2 = Lock()

    threads = [threading.Thread(target=philosopher, args=(i, end)) for i in range (N)]
    for thread in threads :
        thread.start()
    
    time.sleep(100)
    end.value = 0

    print("ending")

    for thread in threads :
        thread.join()

    print(ate)
