import socket
from multiprocessing import Process

def talk(socket, address) :
    print("Connected to client: ", address)
    data = socket.recv(1024)
    while len(data):
        socket.sendall(data)
        data = socket.recv(1024)
    print("Disconnecting from client: ", address)



HOST = "localhost"
PORT = 6666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()
        p = Process(target=talk, args =(client_socket, address,) )
        p.start()
