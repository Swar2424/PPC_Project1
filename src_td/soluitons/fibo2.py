import sys
#import time
from multiprocessing import Process

class FibonacciProcess(Process):
    def __init__(self, n):
        super().__init__()
        self.n = n
    def run(self):
        res = [0]
        a, b = 0, 1
        i = 0
        while i < self.n:
            a, b = b, a+b
            res.append(a)
            i += 1
        print(res)
        #time.sleep(10)
    
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
       
    child = FibonacciProcess(index)
    child.start()
    child.join()
    


