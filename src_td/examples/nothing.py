import signal
 
def handler(sig, frame):
    if sig == signal.SIGINT:
        print("}:-)")
 
signal.signal(signal.SIGINT, handler)
 
while True:
    pass
