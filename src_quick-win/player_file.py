from multiprocessing import shared_memory
import socket
import numpy as np
import sysv_ipc




def send_info(player, info, value, N, message_queue) :
    
    if info == 0 :
        message = "0 0 0"
        
    else :
        message = f"{player} {info} {value}"
    
    for i in range(N-1) :
        message_queue.send((message).encode(), type = 1)
        
        
        
def print_hand(i, hand, colors) :
    print(f"Player {i+1} -> ", end = "")
    for num in hand :
        if num == 0 :
            print(" -- ; ", end = "")

        else :
            color = colors[num//10]
            x = num%10
            print(f"{x} {color} ; ", end = "")
    print()

    
def print_card(num, colors) :
    if num == 0 :
        print(" -- ")

    else :
        color = colors[num//10]
        x = num%10
        print(f"{x} {color}")
    

def print_info(info, colors, hand) :
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(" --- Intel :")
    has_printed = False
    print(f"Player {int(info[0])+1} :")

    if int(info[1]) == 1 :
        for i in range(len(hand)) :
            if hand[i]//10 == int(info[2]) :
                print( f"Card n°{i+1} is {colors[int(info[2])]}")
                has_printed = True
        if not has_printed :
            print(f"No {colors[int(info[2])]} card")
                
    elif int(info[1]) == 2 :
        for i in range(len(hand)) :
            if hand[i]%10 == int(info[2]) :
                print(f"Card n°{i+1} is a {int(info[2])}")
                has_printed = True
        if not has_printed :
            print(f"No {int(info[2])}")




#def player(i, deck_queue, message_queue, suits, hands, colors, joueur, info_token, fuse_token, end) :

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8104
    player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player_socket.connect((HOST, PORT))

    i = int(player_socket.recv(1024).decode())
    player_socket.sendall(("18").encode())


    BigMessage = player_socket.recv(10240).decode().split("\n")
    
    N = int(BigMessage[0])
    mess_colors = str(BigMessage[1])
    colors = mess_colors.split(" ")


    #Récupération de joueur
    name_joueur = BigMessage[2]
    shm_jr = shared_memory.SharedMemory(name = name_joueur)
    joueur = np.ndarray((1,), dtype=np.int64, buffer=shm_jr.buf)

    #Récupération de info_token
    name_info_token = BigMessage[3]
    shm_it = shared_memory.SharedMemory(name = name_info_token)
    info_token = np.ndarray((1,), dtype=np.int64, buffer=shm_it.buf)

    #Récupération de fuse_token
    name_fuse_token = BigMessage[4]
    shm_ft = shared_memory.SharedMemory(name = name_fuse_token)
    fuse_token = np.ndarray((1,), dtype=np.int64, buffer=shm_ft.buf)

    #Récupération de joueur
    name_end = BigMessage[5]
    shm_end = shared_memory.SharedMemory(name = name_end)
    end = np.ndarray((1,), dtype=np.int64, buffer=shm_end.buf)

    #Récupération des suits
    name_suits = BigMessage[6]
    shm_suits = shared_memory.SharedMemory(name = name_suits)
    suits = np.ndarray((N,), dtype=np.int64, buffer=shm_suits.buf)

    #Récupération des hands
    hands = []
    shm_hands = []
    for j in range (N) :
        name_suit = BigMessage[6+j*2]
        name_hand = BigMessage[7+j]
        shm_hands.append(shared_memory.SharedMemory(name = name_hand))
        hands.append(np.ndarray((5,), dtype=np.int64, buffer=(shm_hands[j]).buf))

    

    info_stock = []

    #Récupération des message queues
    key = 128
    key2 = 228
    deck_queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    message_queue = sysv_ipc.MessageQueue(key2, sysv_ipc.IPC_CREAT)

    for j in range (5) :
        a, _ = deck_queue.receive(type=1)
        hands[i][j] = j+1+10*i


    player_socket.sendall(("11").encode())
    start = player_socket.recv(1024).decode()


    #Wait for all players to be set


    if start == "18" :
        
        while end[0] != 0 :
            
            if joueur[0] != i :
                
                #Attente d'info - et du tour de jeu
                info,_ = message_queue.receive()
                info = info.decode().split(" ")
                if int(info[1]) != 0 :
                    info_stock.append(info)

            else :
                #Début du tour d'un joueur -- Adata = player_socket.recv(1024)ffichage des données
                print("----------------------------------------------------------------------------")
                print("----------------------------------------------------------------------------")
                print(f"\nTurn of Player {i+1} : \n")

                print(f"Info tokens : {info_token[0]}  ;  Fuse tokens : {fuse_token[0]}")

                
                #Affichage des mains des autres joueurs
                for j in range (N) :
                    if j != i :
                        print_hand(j%N, hands[j%N], colors)

                #Affichage de l'intel récupéré
                for info in info_stock :
                    try :
                        print_info(info, colors, hands[int(info[0])])
                    except :
                        pass  
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
                info_stock = []
                
                print("Suits :\n| ", end = "")
                k = 0
                for suit in suits :
                    print(f"{colors[k]} : {suit} |", end = " ")
                    k+=1
                print("\n")
                
                #Inputs du joueur pour son tour
                valide = False
                while not valide :
                    choice = input('Donner une info (i) ou jouer une carte (j) : ')
                    
                    try :
                        if str(choice) == "j" :
                            num = input("Card to play (n°) : ")
                            num = int(num) -1

                            print("Card played : ", end = "")
                            print_card(hands[i][num], colors)
                            player_select = 0
                            value_select = 0
                            c_or_n = 0
                            valide = True
                            mess = str(hands[i][num])
                            #[carte jouée]
                            
                            if deck_queue.current_messages != 0 :
                                a, _ = deck_queue.receive(type=1)
                                hands[i][num] = int(a.decode())

                            else :
                                hands[i][num] = 0
                        
                        elif str(choice) == "i" :
                            player_select = input("Player : ")
                            player_select = int(player_select)-1
                            
                            if (player_select >= N or player_select < 0) or player_select == i or info_token[0] == 0 :
                                print("Invalide !")
                                
                            else :
                                info_given = input("Information : ")

                                mess = "placeholder" #pour tester si une option a fonctionné
                                try :
                                    value_select = int(colors.index(str(info_given)))
                                    if  value_select > N or value_select < 0 :
                                        print("Invalide !")
                                    else :
                                        c_or_n = 1
                                        valide = True
                                        mess = "0"
                                        #[info couleur]
                                except :
                                    pass

                                try :
                                    value_select = int(info_given)
                                    if value_select > 5 or value_select < 1 :
                                        print("Invalide !")
                                    else :
                                        c_or_n = 2
                                        valide = True
                                        mess = "0"
                                        #[info numéro]
                                except :
                                    if mess == "placeholder" :
                                        print("Invalide !")

                        elif str(choice) == "q" :
                            print("BREAK")
                            valide = True
                            mess = "0"
                            player_select = 0
                            value_select = 0
                            c_or_n = 0
                            end[0] = 0
                        else :
                            print("Invalide !")
                    except :
                        print("Invalide !")
                        
                player_socket.sendall(mess.encode())
                
                joueur[0] = (joueur[0] + 1) % N
                send_info(player_select, c_or_n, value_select, N, message_queue)
                

            #Attend le signal de fin de tour    
            continuee = player_socket.recv(1024).decode()
            print(continuee)
        
        shm_ft.close()
        shm_end.close()
        shm_it.close()
        shm_jr.close()
        shm_suits.close()
        for i in range (N) :
            shm_hands[i].close()
        mess = "-1"
        player_socket.sendall(mess.encode())