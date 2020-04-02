import pygame
import time
import random
pygame.init()

#Setting Background Color for the window
background_colour = (255,255,255)

#Setting Width and Height of the Frame or Window
(width, height) = (800, 800)

#Creating window for the game by setting Background Color,Width and Height
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Agar.IO')
screen.fill(background_colour)

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

class GameController:    
    #initial parameters
    def __init__(self):
        self.randomlist=[]

    def updaterandomlist(self,list1):
        self.randomlist=list1

    def getrandomlist(self):
        return self.randomlist
    #Function to generate random points and color sequence
    def refreshpoint(self):
        self.randomlist=[]
        for i in range(200):
            randomele=[random.randrange(0,255),random.randrange(0,255),random.randrange(0,255),random.randrange(0,800),random.randrange(0,800)]
            self.randomlist.append(randomele)

    #Function to redraw the frame by creating random dots(small points) and color
    def redraw(self):
        screen.fill(background_colour)
        for i in range(len(self.randomlist)):
            color=(self.randomlist[i][0],self.randomlist[i][1],self.randomlist[i][2])
            pygame.draw.circle(screen, color, (self.randomlist[i][3],self.randomlist[i][4]), 3)

    #Function to remove dots on collision with userblob
    def removepoints(self,x,y,r):
        for i in self.randomlist:
            if ((i[3] - int(x))**2 + (i[4] - int(y))**2 )< int(r)**2:
                r+=0.5
                self.randomlist.remove(i)
        return r
    
    #refresh points if points less than 100
    def refreshpoints(self):
        if len(self.randomlist)<100:
            self.refreshpoint()

class Game():

    def __init__(self):
        self.counter=0
        self.GameController=GameController()
        self.player=Player((0,0,0))
        self.anotherplayer=[Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))),Player((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))]
        self.network=Network()

    def updatedata(self,fullMsg,gamerunning):

        self.GameController.updaterandomlist(fullMsg[0])
        for i in range(len(fullMsg[1])):
            self.anotherplayer[i].setposition(fullMsg[1][i][0],fullMsg[1][i][1],fullMsg[1][i][2])
            x1,y1,r1=self.player.getposition()
            x2,y2,r2=fullMsg[1][i][0],fullMsg[1][i][1],fullMsg[1][i][2]
            if ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) < ((r1 + r2) * (r1 + r2)):
                if r1<r2:
                    self.player.setposition(x1,y1,0)
                    gamerunning=False
                
        return gamerunning
        
    def run(self):
        
        x=0
        y=0
        r=0
        running = True
        gamerunning=True

        while running:
             
            self.network.send([self.GameController.getrandomlist(),x,y,r])

            fullMsg=self.network.recieve()

            if gamerunning:
                
                gamerunning=self.updatedata(fullMsg,gamerunning)

                self.GameController.redraw()

                for i in range(len(fullMsg[1])):
                    self.anotherplayer[i].run()

                self.GameController.refreshpoints()
                
                text = str(self.counter)
                font = pygame.font.SysFont('Consolas', 30)
                screen.blit(font.render(text, True, (0, 0, 0)), (10, 10))
                
                self.player.run()
                self.player.key_operation()
                x,y,r=self.player.getposition()
                r=self.GameController.removepoints(x,y,r)
                self.player.setposition(x,y,r)

                pygame.display.update()
                
                if self.counter==100:
                    gamerunning=False
            else:
                font = pygame.font.SysFont('Consolas', 60)
                self.network.s.close()
                text="Game Over"
                screen.fill(background_colour)
                screen.blit(font.render(text, True, (0, 0, 0)), (250, 400))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT: 
                    self.counter += 1
                if event.type == pygame.QUIT:
                    self.network.s.close()
                    running = False
                    
class Player:
    
    def __init__(self,color):
        self.x=600
        self.y=600
        self.r=15
        self.color=color
    
    def run(self):
        pygame.draw.circle(screen, self.color,(int(self.x),int(self.y)), int(self.r))
    
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

    def getposition(self):
        return self.x,self.y,self.r

    def setposition(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r

class Network():

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1",5001))

    def send(self,datatobesent):
        msg = pickle.dumps(datatobesent)
        self.s.send(msg)

    def recieve(self):
        msg = self.s.recv(4096)
        fullMsg=pickle.loads(msg)
        return fullMsg
    
if __name__ == "__main__":
    import socket
    import pickle

    AgarIO=Game()
    AgarIO.run()
