from multiprocessing import Semaphore, Value, Lock, Array, Manager, Process, Queue
import time
import random
import threading
from kbhit_file import kbhit_input



def player(i, deck_queue, message_queue, suits, hands, colors, joueur) :
    N = len(hands)
    hands[i].get_lock().acquire()

    for j in range (5) :
        hands[i][j] = deck_queue.get()
    
    hands[i].get_lock().release()
    
    while True :
        while joueur.value != i :
            pass
    
        #Début du tour d'un joueur
        print("--------------------------------------")
        print(f"Joueur {i} : ")
        for j in range (N) :
            hands[j].get_lock().acquire()
            print_hand(j%N, hands[j%N], colors)
            hands[j].get_lock().release()
            
        #Inputs du joueur pour son tour
        valide = False
        while not valide :
            choice = kbhit_input("Donner une info (I) ou jouer une carte (J) : ")
            
            try :
                if str(choice) == "J" :
                    num = int(kbhit_input("Numéro de la carte : "))
                    print(num)
                    print_card(hands[i][num], colors)
                    print("Valide")
                    valide = True
                    #[carte jouée]
                
                elif str(choice) == "I" :
                    player_select = int(kbhit_input("Joueur concerné : "))
                    
                    if player_select > 4 or player_select < 0 :
                        print("Invalide !")
                        
                    else :
                        c_or_n = int(kbhit_input("Couleur (1) ou numéro (2) : "))
                        
                        if c_or_n == 1 :
                            value_color = str(kbhit_input("Color : "))
                            value_select = int(colors.index(value_color))
                            if  value_select > N or value_select < 0 :
                                print("Invalide !")
                            else :
                                print("Valide")
                                valide = True
                                #[info couleur]

                        elif c_or_n == 2 :
                            value_select = int(kbhit_input("Valeur : "))
                            if value_select > 5 or value_select < 1 :
                                print("Invalide !")
                            else :
                                print("Valide")
                                valide = True
                                #[info numéro]
                                
                        else :
                            print("Invalide !")
                else :
                    print("Invalide !")

            except :
                print("Invalide !")
                        
                    


def game() :
    pass


def print_hand(i, hand, colors) :
    print("Player", i, end = " -> ")
    for num in hand :
        color = colors[num//10]
        x = num%10
        print(x, color, end = " ; ")
    print()
    
    
def print_card(num, colors) :
    color = colors[num//10]
    x = num%10
    print(x, color)


if __name__ == "__main__":
    N = 0
    while N < 1 or N > 5 :
        N = int(input("NB players : "))
        
    info_token = Value('i', N+3)
    fuse_token = Value('i', 3)
    deck_queue = Queue()
    message_queue = Queue()
    suits = [Value('i', 0) for i in range (N)]
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
    
    players = [Process(target=player, args=(i, deck_queue, message_queue, suits, hands, colors, joueur)) for i in range (N)]

    for player_process in players :
        player_process.start()