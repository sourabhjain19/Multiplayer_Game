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
s.listen(5)


#start listening
print(f'Listening on port {PORT}')

fullMsg=[]

flag1=1
flag2=1

fullMsg=[]
completedata=[[]]*5
totalcount=0

counter=0

count=0
def on_new_client(c,addr,count):
    global counter,fullMsg,completedata,totalcount
    while True:
        
        if count==0:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)

            completedata[0]=[fullMsg[1],fullMsg[2],fullMsg[3]]
            
            counter=fullMsg[4]

            time.sleep(0.0001)

            tempdata=[fullMsg[0],completedata[1:totalcount]]
            msg = pickle.dumps(tempdata)
            c.send(msg)

        elif count==1:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)
    
            completedata[1]=[fullMsg[1],fullMsg[2],fullMsg[3]]
            
            time.sleep(0.0001)
            
            tempdata=[fullMsg[0],completedata[:1]+completedata[2:totalcount],counter]
            msg = pickle.dumps(tempdata)
            c.send(msg)

        elif count==2:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)

            completedata[2]=[fullMsg[1],fullMsg[2],fullMsg[3]]
            
            time.sleep(0.001)
            
            tempdata=[fullMsg[0],completedata[:2]+completedata[3:totalcount],counter]
            msg = pickle.dumps(tempdata)
            c.send(msg)

        elif count==3:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)

            completedata[3]=[fullMsg[1],fullMsg[2],fullMsg[3]]
            
            time.sleep(0.0001)
            
            tempdata=[fullMsg[0],completedata[:3]+completedata[4:totalcount],counter]
            msg = pickle.dumps(tempdata)
            c.send(msg)

        elif count==4:
            msg = c.recv(4096)
            fullMsg=pickle.loads(msg)

            completedata[4]=[fullMsg[1],fullMsg[2],fullMsg[3]]
            
            time.sleep(0.0001)
            
            tempdata=[fullMsg[0],completedata[:4]+completedata[5:totalcount],counter]
            msg = pickle.dumps(tempdata)
            c.send(msg)
            
while True:
    c, addr = s.accept()
    _thread.start_new_thread(on_new_client,(c,addr,count))
    count+=1
    totalcount+=1

    