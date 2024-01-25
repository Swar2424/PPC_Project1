import socket
from multiprocessing import  Value, Array, Queue, Event, shared_memory
from queue import Empty
from threading import Thread
import random
import numpy as np
import sysv_ipc



def check_card(num, suits, end, fuse_token, info_token):
    valeur = num % 10
    couleur = num // 10

    if valeur == suits[couleur] + 1:
        suits[couleur] += 1
        if suits[couleur] == 5 :
            info_token[0] += 1
        return("Card played successfully\n")

    else :
        if fuse_token[0] == 1:
            end[0] = 0
            return("\n\nLOOSER !\n")
        else :
            fuse_token[0] -= 1
            return("Bad card played\n")


def send_mess_player(mess, player_list) :
    for i in range(len(player_list)):
            player_list[i][0].sendall(mess.encode())
            
            
def round_game(player_list, i, end, deck_queue, suits, info_token, fuse_token, N):
    player_socket = player_list[i][0]
    
    while end[0] != 0 :
        data = player_socket.recv(1024)
        card = int(data.decode())
        
        #Si le jeu n'est pas fini
        if card != -1 :
            
            #Si une info a été donnée
            if card == 0:
                info_token[0] -= 1
                mess_end = "Info given\n"
                
            else : 
                mess_end = check_card(card, suits, end, fuse_token, info_token)

                if suits == [Value('i', 5) for _ in range (N)] :
                    mess_end = "\n\nWINNER !\n"
                    end[0] = 0
                    

                elif deck_queue.current_messages == 0 :
                        mess_end = "\n\nLOOSER !\n"
                        end[0] = 0
            
            send_mess_player(mess_end, player_list)
        
            if end[0] == 0 :
                data = player_socket.recv(1024)
        
    
    



if __name__ == "__main__":
    N = 0
    while N < 1 or N > 5 :
        N = int(input("NB players : "))

    #init des fuse_token
    ft = np.array([3])
    shm_ft = shared_memory.SharedMemory(create=True, size=ft.nbytes)
    fuse_token = np.ndarray(ft.shape, dtype=ft.dtype, buffer=shm_ft.buf)
    fuse_token[:] = ft[:]

    #init des info_token
    it = np.array([N+3])
    shm_it = shared_memory.SharedMemory(create=True, size=it.nbytes)
    info_token = np.ndarray(it.shape, dtype=it.dtype, buffer=shm_it.buf)
    info_token[:] = it[:]

    #init de end
    end_temp = np.array([1])
    shm_end = shared_memory.SharedMemory(create=True, size=end_temp.nbytes)
    end = np.ndarray(end_temp.shape, dtype=end_temp.dtype, buffer=shm_end.buf)
    end[:] = end_temp[:]

    #init des joueurs
    jr = np.array([0])
    shm_jr = shared_memory.SharedMemory(create=True, size=jr.nbytes)
    joueur = np.ndarray(jr.shape, dtype=jr.dtype, buffer=shm_jr.buf)
    joueur[:] = jr[:]

    #init des suites
    suits_init = [np.array([0]) for i in range (N)]
    shm_suits = []
    suits = []
    for i in range (N) :
        shm_suits.append(shared_memory.SharedMemory(create=True, size=(suits_init[i]).nbytes))
        suits.append(np.ndarray((suits_init[i]).shape, dtype=(suits_init[i]).dtype, buffer=(shm_suits[i]).buf))
        suits[i][:] = suits_init[i][:]

    #init des hands
    hands_init = [np.array([0, 0, 0, 0, 0]) for i in range (N)]
    shm_hands = []
    hands = []
    for i in range (N) :
        shm_hands.append(shared_memory.SharedMemory(create=True, size=(hands_init[i]).nbytes))
        hands.append(np.ndarray((hands_init[i]).shape, dtype = (hands_init[i]).dtype, buffer = (shm_hands[i]).buf))
        hands[i][:] = hands_init[i][:]
        

    mess_colors = "Blue Red Yellow Green Orange"
    colors = mess_colors.split(" ")

    #Récupération des message queues
    key = 128
    key2 = 228
    deck_queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    message_queue = sysv_ipc.MessageQueue(key2, sysv_ipc.IPC_CREAT)

    deck = []

    for i in range (N) :
        deck += [i*10 + 1, i*10 + 1, i*10 + 1, i*10 + 2, i*10 + 2, i*10 + 3, i*10 + 3, i*10 + 4, i*10 + 4, i*10 + 5]
    random.shuffle(deck)

    for i in range (N*10) :
        deck_queue.send(str(deck.pop(0)).encode(), type = 1)

    HOST = "localhost"
    PORT = 8093
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        player_list = []
        for _ in range (N):
            (player_socket, address) = server_socket.accept()
            player_socket.sendall(str(len(player_list)).encode())
            mess = player_socket.recv(1024)
            player_list.append((player_socket, address))
        
        #on envoie un message à tous les joueurs pour leur dire qu'ils peuvent commencer la partie
        BigMessage = str(N) + "\n"
        BigMessage += mess_colors + "\n"
        BigMessage += shm_jr.name + "\n"
        BigMessage += shm_it.name + "\n"
        BigMessage += shm_ft.name + "\n"
        BigMessage += shm_end.name + "\n"

        for i in range(N) :
            BigMessage += shm_suits[i].name + "\n"
            BigMessage += shm_hands[i].name + "\n"

        send_mess_player(BigMessage, player_list)
        
        for player_socket, address in player_list :
            a = player_socket.recv(1024)
            if int(a.decode()) != 11 :
                print("PANIK")

        start = "18"
        send_mess_player(start, player_list)

        thread_list = [Thread(target = round_game, args = (player_list, i, end, deck_queue, suits, info_token, fuse_token, N)) for i in range (N)]
        
        for t in thread_list :
            t.start()

        for t in thread_list :
            t.join()

        shm_ft.close()
        shm_ft.unlink()
        shm_end.close()
        shm_end.unlink()
        shm_it.close()
        shm_it.unlink()
        shm_jr.close()
        shm_jr.unlink()
        for i in range (N) :
            shm_hands[i].close()
            shm_suits[i].close()
            shm_hands[i].unlink()
            shm_suits[i].unlink()


