import pygame
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

    #Function to generate random points and color sequence
    def refreshpoint(self):
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

    #Operations to be performed on key press(i.e moving the player Blob)
    def key_operation(self,x,y,r):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (x>50+r or (x>0+r and y>50+r)):
            x-=0.25
        elif keys[pygame.K_RIGHT] and x<width-r:
            x+=0.25
        elif keys[pygame.K_UP] and (y>50+r or (y>0+r and x>50+r)):
            y-=0.25
        elif keys[pygame.K_DOWN] and y<height-r:
            y+=0.25
        return x,y

class Game():

    def __init__(self):
        self.counter=0
        self.GameController=GameController()
        self.player=Player()
        self.font = pygame.font.SysFont('Consolas', 30)

    def run(self):

        running = True
        gamerunning=True
        while running:
            if gamerunning:
                
                self.GameController.redraw()

                text = str(self.counter)
                screen.blit(self.font.render(text, True, (0, 0, 0)), (10, 10))

                self.GameController.refreshpoints()
                
                x,y,r=self.player.getposition()
                self.player.run()
                r=self.GameController.removepoints(x,y,r)

                x,y=self.GameController.key_operation(x,y,r)
                self.player.setposition(x,y,r)

                pygame.display.update()
                
                if self.counter==60:
                    gamerunning=False
            else:
                font = pygame.font.SysFont('Consolas', 60)
                text="Game Over"
                screen.fill(background_colour)
                screen.blit(font.render(text, True, (0, 0, 0)), (250, 400))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT: 
                    self.counter += 1
                if event.type == pygame.QUIT:
                    running = False

class Player:
    def __init__(self):
        self.x=400
        self.y=400
        self.r=15
        self.color=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    def run(self):
        pygame.draw.circle(screen, self.color,(int(self.x),int(self.y)), int(self.r))
    def getposition(self):
        return self.x,self.y,self.r       
    def setposition(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r

if __name__ == "__main__":
    AgarIO=Game()
    AgarIO.run()
