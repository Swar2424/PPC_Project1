from multiprocessing import Process, Manager
    
def fibonacci(n, res):
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, a+b
        res.append(a)
        i += 1   

 
if __name__ == "__main__":
    with Manager() as manager :
        n = int(input("Fibo : "))
        res = manager.list(range(0))

        p = Process(target=fibonacci, args =(n, res) )
        p.start()
        p.join()

        print(res)