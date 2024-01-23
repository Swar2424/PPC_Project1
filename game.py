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
            end.value = 0
        else :
            fuse_token.value -= 1

def round_game(player_socket, address, end, deck_queue, suits, info_token, fuse_token, N):
    data = player_socket.recv(1024)
    card = int(data.decode())
    print(card)
    if card == "0":
        info_token.value -= 1
    else : 
        check_card(card, suits, end, fuse_token)

    if end == 0:
        lose = "999"
        player_socket.sendall(lose.encode())

    elif suits == [Value('i', 5) for _ in range (N)] :
        win = "10000"
        player_socket.sendall(win.encode())

    else :
        if deck_queue.empty():
            player_socket.sendall(lose.encode())

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
        for i in range(N):
            start = "18"
            player_list[i][0].sendall(start.encode())

        for i in range (N) :
            t = Thread(target = round_game, args = (player_list[i][0], player_list[i][1], end, deck_queue, suits, info_token, fuse_token, N))
            t.start()
            t.join()
