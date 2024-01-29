import socket


def answer_needed(data):
    return("LOOSE" not in data and "WINNER" not in data and "Info given" not in data and "Card played" not in data and "Bad card played" not in data)




HOST = "localhost"
PORT = 6667
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    end = False
    
    while end != True :
        data = str(client_socket.recv(10240).decode())
        print(data)
        if answer_needed(str(data)) :
            m = input()
            client_socket.sendall(m.encode())
        elif "WINNER" in data or "LOOSE" in data :
            end = True
    
    client_socket.close()