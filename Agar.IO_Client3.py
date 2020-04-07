import pygame
import random
import socket
import pickle
pygame.init()

background_colour = (255,255,255)
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Agar.IO')
screen.fill(background_colour)

class Network():

    #Intilizing the socket and connecting to server
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1",5001))

    #Send randompoints and this player blob's position to other players
    def send(self,datatobesent):
        msg = pickle.dumps(datatobesent)
        self.s.send(msg)

    #Recieve randompoints and other players blob's position
    def recieve(self):
        msg = self.s.recv(4096)
        fullMsg=pickle.loads(msg)
        return fullMsg

class Player:
    
    #Intilizing the variables 
    def __init__(self,color):
        self.x=200
        self.y=200
        self.r=15
        self.color=color
    
    #Creating the Circular Blob
    def run(self):
        pygame.draw.circle(screen, self.color,(int(self.x),int(self.y)), int(self.r))
    
    #Text on Blob indication this player's blob
    def renderText(self):
        text = "User"
        font = pygame.font.SysFont('Consolas', int(self.r/2))
        screen.blit(font.render(text, True, (255,255, 255)), (int(self.x-self.r/2), int(self.y-(self.r/4))))
    
    #Operations to be performed on key press(i.e moving the player Blob)
    def key_operation(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (self.x>50+self.r or (self.x>0+self.r and self.y>50+self.r)):
            self.x-=0.25
        elif keys[pygame.K_RIGHT] and self.x<width-self.r:
            self.x+=0.25
        elif keys[pygame.K_UP] and (self.y>50+self.r or (self.y>0+self.r and self.x>50+self.r)):
            self.y-=0.25
        elif keys[pygame.K_DOWN] and self.y<height-self.r:
            self.y+=0.25

    #Get the position of blob
    def getposition(self):
        return self.x,self.y,self.r

    #set the position of the blob
    def setposition(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r

class Game():
    #Initialising the variables
    def __init__(self):
        self.counter=0
        self.player=Player((0,0,0))
        self.anotherplayer=[Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))]
        self.network=Network()
        self.randomlist=[]
        self.running=True
        self.gamerunning=True

    #Updating the list of random points
    def updaterandomlist(self,list1):
        self.randomlist=list1

    #Returns the list of random points
    def getrandomlist(self):
        return self.randomlist

    #Redraw all the points on the plane
    def redraw(self):
        screen.fill(background_colour)
        for i in range(len(self.randomlist)):
            color=(self.randomlist[i][0],self.randomlist[i][1],self.randomlist[i][2])
            pygame.draw.circle(screen, color, (self.randomlist[i][3],self.randomlist[i][4]), 3)

    #Update the blobs of all other players
    def updatedata(self,fullMsg):
        self.updaterandomlist(fullMsg[0])
        self.player.r=fullMsg[3]
        for i in range(len(fullMsg[1])):
            self.anotherplayer[i].setposition(fullMsg[1][i][0],fullMsg[1][i][1],fullMsg[1][i][2])
            x1,y1,r1=self.player.getposition()
            x2,y2,r2=fullMsg[1][i][0],fullMsg[1][i][1],fullMsg[1][i][2]
            if ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) < ((r1 + r2) * (r1 + r2)):
                if r1<r2:
                    self.player.setposition(x1,y1,0)
                    self.network.send([self.getrandomlist(),x1,y1,0])
                    self.gamerunning=False
    
    #To draw blob of other players
    def runOtherPlayerBlob(self,fullMsg):
         for i in range(len(fullMsg[1])):
            self.anotherplayer[i].run()

    #Update the Counter
    def updateCounter(self,fullMsg):
        self.counter=fullMsg[2]
        text = str(self.counter)
        font = pygame.font.SysFont('Consolas', 30)
        screen.blit(font.render(text, True, (0, 0, 0)), (10, 10))
        if self.counter==100:
            self.gamerunning=False

    #To check for radius of each player to declare the winner
    def results(self):
        x1,y1,r1=self.player.getposition()
        radius_array=[0]*5
        for i in range(5):
            x2,y2,radius_array[i]=self.anotherplayer[i].getposition()
        if r1>max(radius_array):
            text="Game Over, You WON"
        else:
            text="Game Over, You LOSE"

        font = pygame.font.SysFont('Consolas', 60)
        screen.fill(background_colour)
        screen.blit(font.render(text, True, (0, 0, 0)), (50, 400))

    #Runs the Game
    def run(self):

        while self.running:
            if self.gamerunning:
                x,y,r=self.player.getposition()
                self.network.send([self.getrandomlist(),x,y,r])
                fullMsg=self.network.recieve()
                self.updatedata(fullMsg)
                self.redraw()
                self.runOtherPlayerBlob(fullMsg)
                self.updateCounter(fullMsg)
                self.player.run()
                self.player.key_operation()
                self.player.renderText()
                pygame.display.update()
            else:
                self.results()
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.s.close()
                    self.running = False
                    

if __name__ == "__main__":
    AgarIO=Game()
    AgarIO.run()
