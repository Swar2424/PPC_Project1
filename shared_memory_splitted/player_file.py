from multiprocessing import Value, Lock, Array, Process, Queue, Event, shared_memory
import time
import random
import threading
from queue import Empty
import socket
import numpy as np




def send_info(player, info, value, N, message_queue) :
    
    if info == 0 :
        message = (0,0,0)
        
    else :
        message = (player, info, value)
    
    for i in range(N-1) :
        message_queue.put(message)
        
        
        
def print_hand(i, hand, colors) :
    char = f"Player {i+1} -> "
    for num in hand :
        color = colors[num//10]
        x = num%10
        char += f"{x} {color} ; "
    char += "\n"
    return char
    
    
def print_card(num, colors) :
    color = colors[num//10]
    x = num%10
    return (f"{x} {color}")
    

def print_info(info, colors, hand) :
    char = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
    has_printed = False
    
    if info[1] == 1 :
        for i in range(len(hand)) :
            if hand[i]//10 == info[2] :
                char += f"Card n°{i+1} is {colors[info[2]]}\n"
                has_printed = True
        if not has_printed :
            char += f"No {colors[info[2]]} card\n"
                
    elif info[1] == 2 :
        for i in range(len(hand)) :
            if hand[i]%10 == info[2] :
                char += f"Card n°{i+1} is a {info[2]}\n"
                has_printed = True
        if not has_printed :
            char += f"No {info[2]}\n"
    
    return char


def socket_input(char) :
    print(char)
    mess = input()
    return ("", mess)




#def player(i, deck_queue, message_queue, suits, hands, colors, joueur, info_token, fuse_token, end) :

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8082
    player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player_socket.connect((HOST, PORT))

    i = int(player_socket.recv(1024).decode())
    player_socket.sendall(("18").encode())


    BigMessage = player_socket.recv(10240).decode().split("\n")
    
    N = int(BigMessage[0])
    print(N)
    mess_colors = str(BigMessage[1])
    colors = mess_colors.split(" ")
    print


    #Récupération de joueur
    name_joueur = BigMessage[2]
    shm_jr = shared_memory.SharedMemory(name = name_joueur)
    joueur = np.ndarray((1,), dtype=np.int64, buffer=shm_jr.buf)
    print(joueur)

    #Récupération de info_token
    name_info_token = BigMessage[3]
    shm_it = shared_memory.SharedMemory(name = name_info_token)
    info_token = np.ndarray((1,), dtype=np.int64, buffer=shm_it.buf)
    print(info_token)

    #Récupération de fuse_token
    name_fuse_token = BigMessage[4]
    shm_ft = shared_memory.SharedMemory(name = name_fuse_token)
    fuse_token = np.ndarray((1,), dtype=np.int64, buffer=shm_ft.buf)
    print(fuse_token)

    #Récupération de joueur
    name_end = BigMessage[5]
    shm_end = shared_memory.SharedMemory(name = name_end)
    end = np.ndarray((1,), dtype=np.int64, buffer=shm_end.buf)
    print(end)

    hands = []
    suits = []
    hands_shm = []
    suits_shm = []
    for i in range (N) :
        name_suit = BigMessage[6+i]
        name_hand = BigMessage[6+i+1]
        hands_shm.append(shared_memory.SharedMemory(name = name_hand))
        suits_shm.append(shared_memory.SharedMemory(name = name_suit))
        hands.append(np.ndarray((5,), dtype=np.int64, buffer=hands_shm[i].buf))
        suits.append(np.ndarray((1,), dtype=np.int64, buffer=suits_shm[i].buf))


    print(hands)
    print(suits)

    info_stock = []
    char_mess = ""

    for j in range (5) :
        hands[i][j] = deck_queue.get()


    start = player_socket.recv(1024).decode()


    #Wait for all players to be set


    if start == "18" :
        
        while end[0] != 0 :
            joueur.get_lock().acquire()
            
            if joueur[0] != i :
                
                #Attente d'info - et du tour de jeu
                joueur.get_lock().release()
                info = message_queue.get()
                if info[0] == i and info[1] != 0 :
                    info_stock.append(info)

            else :
                joueur.get_lock().release()
                #Début du tour d'un joueur -- Adata = player_socket.recv(1024)ffichage des données
                char_mess +="----------------------------------------------------------------------------\n"
                char_mess +="----------------------------------------------------------------------------\n"
                char_mess +=f"\nTurn of Player {i+1} : \n\n"

                char_mess +=f"Info tokens : {info_token[0]}  ;  Fuse tokens : {fuse_token[0]}\n"

                
                #Affichage des mains des autres joueurs
                for j in range (N) :
                    if j != i :
                        hands[j].get_lock().acquire()
                        char_mess += print_hand(j%N, hands[j%N], colors)
                        hands[j].get_lock().release()

                #Affichage de l'intel récupéré
                for info in info_stock :
                    try :
                        hands[i].get_lock().acquire()
                        char_mess += print_info(info, colors, hands[i])
                        hands[i].get_lock().release()
                    except :
                        pass  
                char_mess +="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n"
                
                char_mess +="Suits :\n| "
                k = 0
                for suit in suits :
                    char_mess +=f"{colors[k]} : {suit} |"
                    k+=1
                char_mess +="\n\n"
                
                #Inputs du joueur pour son tour
                valide = False
                while not valide :
                    char_mess, choice = socket_input(char_mess +'Donner une info (I) ou jouer une carte (J) : ')
                    
                    try :
                        if str(choice) == "J" :
                            char_mess, num = socket_input(char_mess + "Numéro de la carte : ")
                            num = int(num) -1
                            char_mess +="Card played : "
                            char_mess += print_card(hands[i][num], colors) + "\n"
                            valide = True
                            player_select = 0
                            value_select = 0
                            c_or_n = 0
                            #[carte jouée]
                            mess = str(hands[i][num])
                            hands[i][num] = deck_queue.get()
                        
                        elif str(choice) == "I" :
                            char_mess, player_select = socket_input(char_mess + "Player : ")
                            player_select = int(player_select)-1
                            
                            if (player_select >= N or player_select < 0) or player_select == i or info_token[0] == 0 :
                                char_mess +="Invalide !\n"
                                
                            else :
                                char_mess, c_or_n = socket_input(char_mess + "Color (1) or value (2) : ")
                                c_or_n = int(c_or_n)
                                
                                if c_or_n == 1 :
                                    char_mess, value_color = socket_input(char_mess + "Color : ")
                                    value_select = int(colors.index(str(value_color)))
                                    if  value_select > N or value_select < 0 :
                                        char_mess +="Invalide !\n"
                                    else :
                                        valide = True
                                        mess = "0"
                                        #[info couleur]

                                elif c_or_n == 2 :
                                    char_mess, value_select = socket_input(char_mess + "Value : ", )
                                    value_select = int(value_select)
                                    if value_select > 5 or value_select < 1 :
                                        char_mess +="Invalide !\n"
                                    else :
                                        valide = True
                                        mess = "0"
                                        #[info numéro]
                                        
                                else :
                                    char_mess +="Invalide !\n"
                        else :
                            char_mess +="Invalide !\n"

                    except :
                        char_mess +="Invalide !\n"  
                        
                player_socket.sendall(mess.encode())
                send_info(player_select, c_or_n, value_select, N, message_queue)
                
                joueur.get_lock().acquire()
                joueur[0] = (joueur[0] + 1) % N
                joueur.get_lock().release() 
                
            #Attend le signal de fin de tour    
            continuee = player_socket.recv(1024).decode()
            char_mess += continuee
            print(char_mess)
            char_mess = ""
        
        mess = "-1"
        player_socket.sendall(mess.encode())
            
                        
                    


    