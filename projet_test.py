from multiprocessing import Semaphore, Value, Lock, Array, Manager
import time
import random
import threading


def player(i, deck_shuffle, lock) :
    lock.acquire()
    print(i)
    hands[i] = deck_shuffle[1]
    print(i, hands[i])
    lock.release()


def game() :
    pass


if __name__ == "__main__":
    N = int(input("NB players : "))
    players = [threading.Thread(target=player, args=(i,)) for i in range (N)]
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)
    
    with Manager() as manager :
        deck = []
        deck_shuffle = manager.list(range(N*10))
        lock = Lock()
        suits = [manager.list(range(0)) for i in range (N)]
        hands = [manager.list(range(0)) for i in range (N)]

        for i in range (N) :
            deck.append(1)
            deck.append(1)
            deck.append(1)
            deck.append(2)
            deck.append(2)
            deck.append(3)
            deck.append(3)
            deck.append(4)
            deck.append(4)
            deck.append(5)

        for i in range (N*10) :
            a = random.randint(0, len(deck)-1)
            deck_shuffle[i] = deck.pop(a)

        print(deck_shuffle)

        for i in range (N) :
            thread = threading.Thread(target=player, args=(i, deck_shuffle, lock))
            thread.start()