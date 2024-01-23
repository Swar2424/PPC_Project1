from multiprocessing import Semaphore, Value, Lock, Array, Manager, Process, Queue, JoinableQueue
import time
import random
import threading
from kbhit_file import kbhit_input, kbhit_input_long
from queue import Empty
import player_file


if __name__ == "__main__":
    N = 0
    while N < 1 or N > 5 :
        N = int(input("NB players : "))
        
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)
    
    deck_queue = JoinableQueue()
    message_queue = Queue()
    suits = [Value('i', 0) for i in range (N)]
    end = Value('i', 0) #variabnle qui indique si le jeu continue (0) ou s'il s'arrête (1)

    hands = [Array('i', range(5)) for i in range (N)]
    joueur = Value('i', 0)
    
    colors = ["Blue", "Red", "Yellow", "Green", "Orange"]
    deck = []

    #Construction du _shuffle à l'aide de deck
    for i in range (N) :
        deck += [i*10 + 1, i*10 + 1, i*10 + 1, i*10 + 2, i*10 + 2, i*10 + 3, i*10 + 3, i*10 + 4, i*10 + 4, i*10 + 5]
    
    for i in range (N*10) :
        a = random.randint(0, len(deck)-1)
        deck_queue.put(deck.pop(a))
    
    players = [Process(target=player_file.player, args=(i, deck_queue, message_queue, suits, hands, colors, joueur, info_token, fuse_token)) for i in range (N)]

    for player_process in players :
        player_process.start()
    