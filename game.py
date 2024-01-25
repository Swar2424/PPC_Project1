import socket
from multiprocessing import  Value, Array, Queue, Event
from queue import Empty
from threading import Thread
import random


def check_card(num, suits, end, fuse_token, info_token):
    valeur = num % 10
    couleur = num // 10

    if valeur == suits[couleur].value + 1:
        suits[couleur].value += 1
        if suits[couleur].value == 5 :
            info_token.value += 1
        return("Card played successfully\n")

    else :
        if fuse_token.value == 1:
            end.value = 0
            return("\n\nLOOSER !\n")
        else :
            fuse_token.value -= 1
            return("Bad card played\n")


def send_mess_player(mess, player_list) :
    for i in range(len(player_list)):
            player_list[i][0].sendall(mess.encode())
            
            
def round_game(player_list, i, end, deck_queue, suits, info_token, fuse_token, N):
    player_socket = player_list[i][0]
    
    while end.value != 0 :
        data = player_socket.recv(1024)
        card = int(data.decode())
        
        #Si le jeu n'est pas fini
        if card != -1 :
            
            #Si une info a été donnée
            if card == 0:
                info_token.value -= 1
                mess_end = "Info given\n"
                
            else : 
                mess_end = check_card(card, suits, end, fuse_token, info_token)

                if suits == [Value('i', 5) for _ in range (N)] :
                    mess_end = "\n\nWINNER !\n"
                    end.value = 0
                    

                elif deck_queue.empty():
                        mess_end = "\n\nLOOSER !\n"
                        end.value = 0
            
            send_mess_player(mess_end, player_list)
        
            if end.value == 0 :
                data = player_socket.recv(1024)
        
    
    



def game(end, deck_queue, suits, info_token, fuse_token, N, start) :

    #Construction du _shuffle à l'aide de deck
    deck = []

    for i in range (N) :
        deck += [i*10 + 1, i*10 + 1, i*10 + 1, i*10 + 2, i*10 + 2, i*10 + 3, i*10 + 3, i*10 + 4, i*10 + 4, i*10 + 5]
    random.shuffle(deck)

    for i in range (N*10) :
        deck_queue.put(deck.pop(0))

    #Les joueurs peuvent commencer à piocher
    start.set()

    HOST = "localhost"
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        player_list = []
        for _ in range (N):
            (player_socket, address) = server_socket.accept()
            player_list.append((player_socket, address))
        
        #on envoie un message à tous les joueurs pour leur dire qu'ils peuvent commencer la partie
        start = "18"
        send_mess_player(start, player_list)

        thread_list = [Thread(target = round_game, args = (player_list, i, end, deck_queue, suits, info_token, fuse_token, N)) for i in range (N)]
        
        for t in thread_list :
            t.start()

