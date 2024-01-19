from multiprocessing import Process, Pipe
    
def reverse(conn):
    while True :
        word = conn.recv()
        conn.send(word[::-1])

 
if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    End = False
    p = Process(target=reverse, args =(child_conn,) )
    p.start()

    while not End :
        word = str(input("Mot : "))
        if word != "end" :
            parent_conn.send(word)
            print(parent_conn.recv())

        else :
            print("the end")
            parent_conn.close()
            child_conn.close()
            p.terminate()
            End = True

    p.join()

