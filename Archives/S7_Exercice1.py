from multiprocessing import Lock
import time
import random
import threading

 
def philosopher(i, chopstick):
    while True:
        think()

        left_stick = i
        right_stick = (i + 1) % N

        if i%2 == 1 :
            chopstick[left_stick].acquire()
            chopstick[right_stick].acquire()
        else :
            chopstick[right_stick].acquire() 
            chopstick[left_stick].acquire()
            
        eat(i)

        chopstick[left_stick].release()
        chopstick[right_stick].release()


def think() :
    time.sleep(random.random()/10)


def eat(i) :
    print(f"{i} is eating")
    time.sleep(random.random()/10)
    print(f"{i} stopped")


if __name__ == "__main__":
    N = 5
    chopstick = [Lock() for i in range(N)]

    for i in range (N) :
        thread = threading.Thread(target=philosopher, args=(i, chopstick))
        thread.start()
