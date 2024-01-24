import socket
from multiprocessing import  Value, Array, Queue
from queue import Empty
from threading import Thread


def check_card(num, suits, end, fuse_token):
    valeur = num % 10
    couleur = num // 10
    if valeur == suits[couleur].value + 1:
        suits[couleur].value += 1
    else : 
        if fuse_token.value == 0:
            print("- - - - - - - - - - - - - - - - -\n          LOOOOOOOOOOOOOOOOOOOOOOOSER !\n- - - - - - - - - - - - - - - - -")
            end.value = 0
        else :
            fuse_token.value -= 1


def send_mess_player(mess, player_list) :
    for i in range(len(player_list)):
            player_list[i][0].sendall(mess.encode())
            
            
def round_game(player_list, i, end, deck_queue, suits, info_token, fuse_token, N):
    player_socket = player_list[i][0]
    
    while end.value != 0 :
        data = player_socket.recv(1024)
        card = int(data.decode())
        
        if card != -1 :
        
            if card == 0:
                info_token.value -= 1
                
            else : 
                check_card(card, suits, end, fuse_token)

                if suits == [Value('i', 5) for _ in range (N)] :
                    print("- - - - - - - - - - - - - - - - -\n          WINNNNNNNNNNNNNNNNNNNNNNER\n- - - - - - - - - - - - - - - - -")
                    end.value = 0
                    

                elif deck_queue.empty():
                        print("- - - - - - - - - - - - - - - - -\n          LOOOOOOOOOOOOOOOOOOOOOOOSER !\n- - - - - - - - - - - - - - - - -")
                        end.value = 0
            
            mess = "19"
            send_mess_player(mess, player_list)
        
            if end.value == 0 :
                data = player_socket.recv(1024)
        
    
    



def game(end, deck_queue, suits, info_token, fuse_token, N) :

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

