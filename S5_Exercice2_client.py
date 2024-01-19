import sys
import socket
 
def user():
    answer = 3
    while answer not in [1, 2]:
        print("1. to get current date/time")
        print("2. to terminate time server")
        answer = int(input())
    return answer
 
HOST = "localhost"
PORT = 6679
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    end = False
    while not end :
        m = user()
        if m == 1:
            client_socket.send(b"1")
            print("sent")
            resp = client_socket.recv(1024)
            if not len(resp):
                print("The socket connection has been closed!")
                sys.exit(1)
            print("Server response:", resp.decode())
        if m == 2:
            print("the end")
            client_socket.send(b"2")
            end = True