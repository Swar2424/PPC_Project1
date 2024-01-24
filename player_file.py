from multiprocessing import Semaphore, Value, Lock, Array, Manager, Process, Queue, JoinableQueue
import time
import random
import threading
from kbhit_file import kbhit_input, kbhit_input_long
from queue import Empty
import socket



def player(i, deck_queue, message_queue, suits, hands, colors, joueur, info_token, fuse_token, end) :
    N = len(hands)
    info_stock = []
    
    hands[i].get_lock().acquire()
    for j in range (5) :
        hands[i][j] = deck_queue.get()
    hands[i].get_lock().release()
    #print_hand(i, hands[i], colors)

    #Wait for all players to be set
    HOST = "localhost"
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player_socket :
        player_socket.connect((HOST, PORT))
        start = player_socket.recv(1024).decode()

        if start == "18" :
    
            while end.value != 0 :
                joueur.get_lock().acquire()
                
                if joueur.value != i :
                    
                    #Attente d'info - et du tour de jeu
                    joueur.get_lock().release()
                    info = message_queue.get()
                    if info[0] == i and info[1] != 0 :
                        info_stock.append(info)

                else :
                    joueur.get_lock().release()
                    #Début du tour d'un joueur -- Affichage des données
                    print("----------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------")
                    print(f"Turn of Player {i+1} : ")
                    print()
                    print(f"Info tokens : {info_token.value}  ;  Fuse tokens : {fuse_token.value}")
                    print()
                    
                    #Affichage des mains des autres joueurs
                    for j in range (N) :
                        if j != i :
                            hands[j].get_lock().acquire()
                            print_hand(j%N, hands[j%N], colors)
                            hands[j].get_lock().release()

                    #Affichage de l'intel récupéré
                    for info in info_stock :
                        try :
                            hands[i].get_lock().acquire()
                            print_info(info, colors, hands[i])
                            hands[i].get_lock().release()
                        except :
                            pass  
                    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                    
                    print()
                    print("Suits :", end = "\n| ")
                    k = 0
                    for suit in suits :
                        print(colors[k], ":", suit.value, end =" | ")
                        k+=1
                    print()
                    print()
                    
                    #Inputs du joueur pour son tour
                    valide = False
                    while not valide :
                        choice = kbhit_input("Donner une info (I) ou jouer une carte (J) : ")
                        
                        try :
                            if str(choice) == "J" :
                                num = int(kbhit_input("Numéro de la carte : ")) - 1
                                print("Card played : ", end = "")
                                print_card(hands[i][num], colors)
                                valide = True
                                player_select = 0
                                value_select = 0
                                c_or_n = 0
                                #[carte jouée]
                                mess = str(hands[i][num])
                                hands[i][num] = deck_queue.get()
                            
                            elif str(choice) == "I" :
                                player_select = int(kbhit_input("Player : ")) - 1
                                
                                if (player_select >= N or player_select < 0) or player_select == i :
                                    print("Invalide !")
                                    
                                else :
                                    c_or_n = int(kbhit_input("Color (1) or value (2) : "))
                                    
                                    if c_or_n == 1 :
                                        value_color = str(kbhit_input_long("Color : "))
                                        value_select = int(colors.index(value_color))
                                        if  value_select > N or value_select < 0 :
                                            print("Invalide !")
                                        else :
                                            valide = True
                                            mess = "0"
                                            #[info couleur]

                                    elif c_or_n == 2 :
                                        value_select = int(kbhit_input("Value : "))
                                        if value_select > 5 or value_select < 1 :
                                            print("Invalide !")
                                        else :
                                            valide = True
                                            mess = "0"
                                            #[info numéro]
                                            
                                    else :
                                        print("Invalide !")
                            else :
                                print("Invalide !")

                        except :
                            print("Invalide !")  
                         
                    player_socket.sendall(mess.encode())
                    send_info(player_select, c_or_n, value_select, N, message_queue)
                    
                    joueur.get_lock().acquire()
                    joueur.value = (joueur.value + 1) % N
                    joueur.get_lock().release() 
                    
                #Attend le signal de fin de tour    
                continuee = player_socket.recv(1024).decode()
                
                if continuee != "19" :
                    end.value = 0
                    print(i, "PANIK")
            
            mess = "-1"
            player_socket.sendall(mess.encode())
            
                        
                    

def send_info(player, info, value, N, message_queue) :
    
    if info == 0 :
        message = (0,0,0)
        
    else :
        message = (player, info, value)
    
    for i in range(N-1) :
        message_queue.put(message)
        
        
        
def print_hand(i, hand, colors) :
    print("Player", i+1, end = " -> ")
    for num in hand :
        color = colors[num//10]
        x = num%10
        print(x, color, end = " ; ")
    print()
    
    
def print_card(num, colors) :
    color = colors[num//10]
    x = num%10
    print(x, color)
    

def print_info(info, colors, hand) :
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    has_printed = False
    
    if info[1] == 1 :
        for i in range(len(hand)) :
            if hand[i]//10 == info[2] :
                print(f"Card n°{i+1} is {colors[info[2]]}")
                has_printed = True
        if not has_printed :
            print(f"No {colors[info[2]]} card")
                
    elif info[1] == 2 :
        for i in range(len(hand)) :
            if hand[i]%10 == info[2] :
                print(f"Card n°{i+1} is a {info[2]}")
                has_printed = True
        if not has_printed :
            print(f"No {info[2]}")