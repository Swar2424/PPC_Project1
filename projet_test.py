from multiprocessing import Semaphore, Value, Lock, Array, Manager, Process
import socket
import time
import random
import threading



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

def check_card(num, suits, end, fuse_token):
    valeur = num % 10
    couleur = num // 10
    if valeur == suits[couleur].value + 1:
        suits[couleur].value += 1
    else : 
        if fuse_token.value == 0:
            end.value = 0
        else :
            fuse_token.value -= 1

def game(end, deck_shuffle, suits, info_token, fuse_token, carte_piochee) :
   i = 0
   while end.value != 1:
    parent_conn, child_conn = 0, 0
    joueur_a_joué_une_carte = True
    if joueur_a_joué_une_carte == True: 
        check_card(num, suits, end, fuse_token)
    else :
        info_token.value -= 1
    if end == 0 :
        inbdhzbd = 1
        #envoyer message en socket : vous avez tous perdu
    elif suits == [Value('i', 5) for j in range (N)] :
        print("Vous avez gagné")

    else :
        deck_shuffle.array.remove(carte_piochee)
        if deck_shuffle.array == []:
            #envoyer un message pour dire qu'ils ont perdu

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