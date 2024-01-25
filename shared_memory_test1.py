import socket
from multiprocessing import shared_memory
import numpy as np


HOST = "localhost"
PORT = 6666
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    
    data = str(client_socket.recv(10240).decode())
    print(data)
    existing_shm = shared_memory.SharedMemory(name = data)
    c = np.ndarray((6,), dtype=np.int64, buffer=existing_shm.buf)
    print(c)

    c[2] = 666
    m = "18"
    client_socket.sendall(m.encode())

    del(c)
    existing_shm.close()
    existing_shm.unlink()
    client_socket.close()