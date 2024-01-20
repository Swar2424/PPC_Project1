from multiprocessing import Semaphore, Value, Lock, Array, Manager
import time
import random
import threading


def player(i, hands) :
    lock.acquire()
    for j in range (5) :
        a = deck_counter.value
        hands[i][j] = deck_shuffle[a]
        deck_counter.value += 1
    lock.release()
    print(i, hands[i])


def game() :
    pass


if __name__ == "__main__":
    N = int(input("NB players : "))
    players = [threading.Thread(target=player, args=(i,)) for i in range (N)]
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)

    deck = []
    deck_shuffle = Array('i', range(N*10))
    deck_counter = Value('i', 0)
    lock = Lock()
    suits = [Array('i', range(5)) for i in range (N)]
    hands = [Array('i', range(5)) for i in range (N)]

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
        thread = threading.Thread(target=player, args=(i, hands),)
        thread.start()