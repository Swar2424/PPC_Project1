import socket
from multiprocessing import shared_memory   

    
    
HOST_int = "localhost"
PORT_int = 6666 + i
shared_mem = shared_memory.SharedMemory(create=True, size=a.nbytes)
mess = shared_mem.name

server_socket_int = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_int.bind((HOST_int, PORT_int))
server_socket_int.listen(1)
client_socket_int, address = server_socket_int.accept()
client_socket_int.sendall(mess.encode())
conf = client_socket_int.recv(1024).decode()