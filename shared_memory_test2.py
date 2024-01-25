import socket
from multiprocessing import shared_memory
import numpy as np

    
    
HOST_int = "localhost"
PORT_int = 6666



a = np.array([1, 1, 2, 3, 5, 8])
shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
b[:] = a[:]
mess = shm.name
print(b)


server_socket_int = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_int.bind((HOST_int, PORT_int))
server_socket_int.listen(1)
client_socket_int, address = server_socket_int.accept()
client_socket_int.sendall(mess.encode())
conf = client_socket_int.recv(1024).decode()

print(b)

del(b)
shm.close()
shm.unlink()