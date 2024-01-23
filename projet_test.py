from multiprocessing import Semaphore, Value, Lock, Array, Manager, Process
import game
import time
import random



def player(i, deck_counter, deck_shuffle, suits, hands) :
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


if __name__ == "__main__":
    N = int(input("NB players : "))
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)
    end = Value('i', 0) #variabnle qui indique si le jeu continue (0) ou s'il s'arrête (1)
    deck = []
    deck_shuffle = Array('i', range(N*10))
    deck_counter = Value('i', 0)
    suits = [Value('i', 0) for i in range (N)] #toutes les piles sont à 0
    hands = [Array('i', range(5)) for i in range (N)]
    
    players = [Process(target=player, args=(i, deck_counter, deck_shuffle, suits, hands)) for i in range (N)]

    #Construction du _shuffle à l'aide de deck
    for i in range (N) :
        deck += [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
    
    for i in range (N*10) :
        a = random.randint(0, len(deck)-1)
        deck_shuffle[i] = deck.pop(a)

    for player_process in players :
        player_process.start()
    