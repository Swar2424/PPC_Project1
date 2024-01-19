import time
import random
import multiprocessing
from math import sqrt
 
def primality(n):
    if n < 2:
        return (n, False)
    if n == 2:
        return (n, True)
    if n % 2 == 0:
        return (n, False)

    for i in range (3, round(sqrt(n))+1, 2) :
        if n%i == 0 :
            return (n, False)
    return (n, True)
 
if __name__ == "__main__":
    start = time.time()
    indexes = [random.randint(10000, 10000000) for i in range(100000)]
 
    with multiprocessing.Pool(processes = 15) as pool:
        for x in pool.map_async(primality, indexes).get():
            pass
    
    end = time.time()
    print(end - start)