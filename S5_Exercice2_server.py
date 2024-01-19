import select
import socket
import time
from multiprocessing import Process
import concurrent.futures
 
serve = True
 
def time_send(socket) :
    print("start_request")
    end = False
    while not end :
        data = socket.recv(1024)
        if data == b'1':
            socket.sendall(str(time.asctime()).encode())
            print("send")
        else : 
            end = True
            socket.close()
            print("the end")


HOST = "localhost"
PORT = 6679

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    server_socket.setblocking(False)

    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
    
        while serve:
            time.sleep(1)
            readable, writable, error = select.select([server_socket], [], [], 1)
            if server_socket in readable: # if server_socket is ready
                client_socket, address = server_socket.accept() # will return immediately
                executor.submit(time_send, client_socket,)