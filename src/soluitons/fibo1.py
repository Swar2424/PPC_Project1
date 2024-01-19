import os
import sys
import time
from multiprocessing import Process

def fibonacci(n):
    res = [0]
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, a+b
        res.append(a)
        i += 1
    print(res)
    print("In process:", os.getpid(), ", child process of process:", os.getppid())
    time.sleep(20)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("required index argument missing, terminating.", file=sys.stderr)
        sys.exit(1)
        
    try:
        index = int(sys.argv[1])
    except ValueError:
        print("bad index argument: {}, terminating.".format(sys.argv[1]), file=sys.stderr)
        sys.exit(2)
        
    if index < 0:
        print("negative index argument: {}, terminating.".format(index), file=sys.stderr)
        sys.exit(3)
       
    child = Process(target=fibonacci, args=(index,))
    child.start()
    child.join()
    print("In process:", os.getpid(), ", child process of process:", os.getppid())
    
    


