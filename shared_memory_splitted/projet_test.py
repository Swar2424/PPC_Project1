from multiprocessing import Value, Lock, Array, Process, Queue, Event
import time
import random
import threading
from kbhit_file import kbhit_input, kbhit_input_long
from queue import Empty
import player_file
import game


if __name__ == "__main__":
    N = 0
    while N < 1 or N > 5 :
        N = int(input("NB players : "))
        
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)
    deck_queue = Queue()
    message_queue = Queue()
    suits = [Value('i', 0) for i in range (N)]
    end = Value('i', 0) #variable qui indique si le jeu continue (0) ou s'il s'arrête (1)
    start = Event()

    hands = [Array('i', range(5)) for i in range (N)]
    joueur = Value('i', 0)
    end = Value('i', 1)
    
    colors = ["Blue", "Red", "Yellow", "Green", "Orange"]
    
    game_start = Process(target=game.game, args= (end, deck_queue, suits, info_token, fuse_token, N, start))
    game_start.start()

    players = [Process(target=player_file.player, args=(i, deck_queue, message_queue, suits, hands, colors, joueur, info_token, fuse_token, end, start)) for i in range (N)]

    for player_process in players :
        player_process.start()