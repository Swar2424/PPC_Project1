from multiprocessing import Semaphore, Value, Lock, Array, Manager
import time
import random
import threading


def player(i) :
    pass


def game() :
    pass


if __name__ == "__main__":
    N = int(input("NB players : "))
    players = [threading.Thread(target=player, args=(i,)) for i in range (N)]
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)
    
    with Manager() as manager :
        deck = manager.list(range(0))
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
        print(deck)