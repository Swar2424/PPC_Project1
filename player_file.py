from multiprocessing import Value, Lock, Array, Process, Queue, Event
import time
import random
import threading
from kbhit_file import kbhit_input, kbhit_input_long
from queue import Empty
import socket



def player(i, deck_queue, message_queue, suits, hands, colors, joueur, info_token, fuse_token, end, start) :
    N = len(hands)
    info_stock = []
    char_mess = ""

    start.wait()
    
    hands[i].get_lock().acquire()
    for j in range (5) :
        hands[i][j] = deck_queue.get()
    hands[i].get_lock().release()
    
    HOST_int = "localhost"
    PORT_int = 6666 + i

    server_socket_int = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_int.bind((HOST_int, PORT_int))
    server_socket_int.listen(1)
    client_socket_int, address = server_socket_int.accept()
    mess = f"Player {i+1} connected - send (1) to confirm"
    client_socket_int.sendall(mess.encode())
    conf = client_socket_int.recv(1024).decode()
    

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
                    #Début du tour d'un joueur -- Adata = player_socket.recv(1024)ffichage des données
                    char_mess +="----------------------------------------------------------------------------\n"
                    char_mess +="----------------------------------------------------------------------------\n"
                    char_mess +=f"\nTurn of Player {i+1} : \n\n"

                    char_mess +=f"Info tokens : {info_token.value}  ;  Fuse tokens : {fuse_token.value}\n"

                    
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
                        char_mess +=f"{colors[k]} : {suit.value} |"
                        k+=1
                    char_mess +="\n\n"
                    
                    #Inputs du joueur pour son tour
                    valide = False
                    while not valide :
                        char_mess, choice = socket_input(char_mess +'Donner une info (I) ou jouer une carte (J) : ', client_socket_int)
                        
                        try :
                            if str(choice) == "J" :
                                char_mess, num = socket_input(char_mess + "Numéro de la carte : ", client_socket_int)
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
                                char_mess, player_select = socket_input(char_mess + "Player : ", client_socket_int)
                                player_select = int(player_select)-1
                                
                                if (player_select >= N or player_select < 0) or player_select == i or info_token.value == 0 :
                                    char_mess +="Invalide !\n"
                                    
                                else :
                                    char_mess, c_or_n = socket_input(char_mess + "Color (1) or value (2) : ", client_socket_int)
                                    c_or_n = int(c_or_n)
                                    
                                    if c_or_n == 1 :
                                        char_mess, value_color = socket_input(char_mess + "Color : ", client_socket_int)
                                        value_select = int(colors.index(str(value_color)))
                                        if  value_select > N or value_select < 0 :
                                            char_mess +="Invalide !\n"
                                        else :
                                            valide = True
                                            mess = "0"
                                            #[info couleur]

                                    elif c_or_n == 2 :
                                        char_mess, value_select = socket_input(char_mess + "Value : ", client_socket_int)
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
                    joueur.value = (joueur.value + 1) % N
                    joueur.get_lock().release() 
                    
                #Attend le signal de fin de tour    
                continuee = player_socket.recv(1024).decode()
                char_mess += continuee
                client_socket_int.sendall(char_mess.encode())
                char_mess = ""
            
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



def socket_input(char, client_socket) :
    client_socket.sendall(char.encode())
    mess = client_socket.recv(1024).decode()
    return ("", mess)
    