import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key)
 
value = 1
while value:
    act = int(input("Action ? "))

    if act == 1 :
        message = mq.send(b"mes", type=1)
        message, t = mq.receive([False, [3]])
        print(message.decode())
    else :
        message = mq.send(b"mes", type=2)
        value = 0