from multiprocessing import Semaphore, Value, Lock, Array, Manager
import time
import random
import threading


def player(i) :
    deck_counter.get_lock().acquire()
    print(i, end = " ")
    for j in range (5) :
        a = deck_counter.value
        hands[i][j] = deck_shuffle[a]
        deck_counter.value += 1
    for j in range (5) :
        print(hands[i][j], end = " ")
    print("")
    deck_counter.get_lock().release()


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
    suits = [Array('i', range(5)) for i in range (N)]
    hands = [Array('i', range(5)) for i in range (N)]

    #Construction du _shuffle à l'aide de deck
    for i in range (N) :
        deck += [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
    
    for i in range (N*10) :
        a = random.randint(0, len(deck)-1)
        deck_shuffle[i] = deck.pop(a)

    for i in range (N) :
        thread = threading.Thread(target=player, args=(i,),)
        thread.start()