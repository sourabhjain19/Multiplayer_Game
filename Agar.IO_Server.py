import socket
import time
import pickle
import _thread
import random
PORT = 5001
class Network():

    #Intilizing the socket and connecting to server
    def __init__(self):
        
        HEADER_LENGTH = 10
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("127.0.0.1",PORT))
        self.s.listen(5)
        print(f'Listening on port {PORT}')
    
    #Send randompoints,other player blob's position,counter to all other players
    def send(self,c,datatobesent):
        msg = pickle.dumps(datatobesent)
        c.send(msg)

    #Recieve randompoints and other players blob's position
    def recieve(self,c):
        msg = c.recv(4096)
        fullMsg=pickle.loads(msg)
        return fullMsg

class GameServer():

    def __init__(self):
        self.randomlist=[]
        self.fullMsg=[]
        self.flag1=1
        self.flag2=1
        self.fullMsg=[]
        self.completedata=[[]]*5
        self.totalcount=0
        self.count=0
        self.counterv=0
        self.netwok=Network()
               
    #Thread to increment the count afer one sec 
    def counter(self):
        while True:
            time.sleep(1)
            self.counterv+=1

    #Refresh the points on the game list
    def refreshpoint(self):
        if len(self.randomlist)<100:
            self.randomlist=[]
            for i in range(200):
                randomele=[random.randrange(0,255),random.randrange(0,255),random.randrange(0,255),random.randrange(0,800),random.randrange(0,800)]
                self.randomlist.append(randomele)

    #Remove the points which lie in areas of player Blob's
    def removepoints(self,rl,x,y,r):
        for i in rl:
            if ((i[3] - int(x))**2 + (i[4] - int(y))**2 )< int(r)**2:
                r+=0.5
                rl.remove(i)
        return rl,r

    #Run this thread after every new client is added to exchage object between client and the server
    def on_new_client(self,c,addr,count):
        while True:

            if count==0:
                self.fullMsg=self.netwok.recieve(c)
                self.completedata[0]=[self.fullMsg[1],self.fullMsg[2],self.fullMsg[3]]
                self.randomlist,r1=self.removepoints(self.fullMsg[0],self.fullMsg[1],self.fullMsg[2],self.fullMsg[3])
                self.refreshpoint()
                time.sleep(0.0001)
                tempdata=[self.randomlist,self.completedata[1:self.totalcount],self.counterv,r1]
                self.netwok.send(c,tempdata)

            elif count==1:
                self.fullMsg=self.netwok.recieve(c)
                self.completedata[1]=[self.fullMsg[1],self.fullMsg[2],self.fullMsg[3]]
                self.randomlist,r2=self.removepoints(self.fullMsg[0],self.fullMsg[1],self.fullMsg[2],self.fullMsg[3])
                self.refreshpoint()
                time.sleep(0.0001)
                tempdata=[self.randomlist,self.completedata[:1]+self.completedata[2:self.totalcount],self.counterv,r2]
                self.netwok.send(c,tempdata)

            elif count==2:
                self.fullMsg=self.netwok.recieve(c)
                self.completedata[2]=[self.fullMsg[1],self.fullMsg[2],self.fullMsg[3]]
                self.randomlist,r3=self.removepoints(self.fullMsg[0],self.fullMsg[1],self.fullMsg[2],self.fullMsg[3])
                self.refreshpoint()
                time.sleep(0.001)
                tempdata=[self.randomlist,self.completedata[:2]+self.completedata[3:self.totalcount],self.counterv,r3]
                self.netwok.send(c,tempdata)

            elif count==3:
                self.fullMsg=self.netwok.recieve(c)
                self.completedata[3]=[self.fullMsg[1],self.fullMsg[2],self.fullMsg[3]]  
                self.randomlist,r4=self.removepoints(self.fullMsg[0],self.fullMsg[1],self.fullMsg[2],self.fullMsg[3])
                self.refreshpoint()
                time.sleep(0.0001)
                tempdata=[self.randomlist,self.completedata[:3]+self.completedata[4:self.totalcount],self.counterv,r4]
                self.netwok.send(c,tempdata)

            elif count==4:
                self.fullMsg=self.netwok.recieve(c)
                self.completedata[4]=[self.fullMsg[1],self.fullMsg[2],self.fullMsg[3]]
                self.randomlist,r5=self.removepoints(self.fullMsg[0],self.fullMsg[1],self.fullMsg[2],self.fullMsg[3])
                self.refreshpoint()
                time.sleep(0.0001)
                self.tempdata=[self.fullMsg[0],self.completedata[:4]+self.completedata[5:self.totalcount],self.counterv,r5]
                self.netwok.send(c,tempdata)
    
    #To run the game server
    def run(self):
        while True:
            c, addr = self.netwok.s.accept()
            if self.count==0:
                _thread.start_new_thread(self.counter,())    
            _thread.start_new_thread(self.on_new_client,(c,addr,self.count))
            self.count+=1
            self.totalcount+=1

if __name__ == "__main__":
    agarIOServer=GameServer()
    agarIOServer.run()