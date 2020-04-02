import socket
import time
import pickle
import _thread

PORT = 5001

#setting the constant to send the data in formatted way
HEADER_LENGTH = 10

#AF_INET -> ipv4, SOCK_STREAM -> tcp connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#gethostname -> refering to self on port 8080
s.bind(("127.0.0.1",PORT))

#request queue of size 5
s.listen(2)


#start listening
print(f'Listening on port {PORT}')

fullMsg=[]

flag1=1
flag2=1

fullMsg=[]
x1,y1,r1=0,0,0
x2,y2,r2=0,0,0

count=1
def on_new_client(c,addr,count):
    global fullMsg,x1,y1,r1,x2,y2,r2
    while True:
        if count==1:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)

            x1=fullMsg[1]
            y1=fullMsg[2]
            r1=fullMsg[3]
            time.sleep(0)
            
            fullMsg[1],fullMsg[2],fullMsg[3]=x2,y2,r2
            msg = pickle.dumps(fullMsg)
            c.send(msg)
        else:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)

            x2,y2,r2=fullMsg[1],fullMsg[2],fullMsg[3]
            time.sleep(0)
            
            fullMsg[1],fullMsg[2],fullMsg[3]=x1,y1,r1
            msg = pickle.dumps(fullMsg)
            c.send(msg)
            
while True:
    c, addr = s.accept()
    _thread.start_new_thread(on_new_client,(c,addr,count))
    count+=1

    