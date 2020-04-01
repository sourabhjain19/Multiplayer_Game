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

#Function to generate random points and color sequence
def refreshpoints():
    randomlist=[]
    for i in range(200):
        randomele=[random.randrange(0,255),random.randrange(0,255),random.randrange(0,255),random.randrange(0,800),random.randrange(0,800)]
        randomlist.append(randomele)
    return randomlist

#Function to redraw the frame by creating random dots(small points) and color
def redraw(randomlist):
    screen.fill(background_colour)

    for i in range(len(randomlist)):
        color=(randomlist[i][0],randomlist[i][1],randomlist[i][2])
        pygame.draw.circle(screen, color, (randomlist[i][3],randomlist[i][4]), 3)

#Function to remove dots on collision with userblob
def removepoints(x,y,r):
    for i in randomlist:
        if ((i[3] - int(x))**2 + (i[4] - int(y))**2 )< int(r)**2:
            r+=0.5
            randomlist.remove(i)
    return randomlist,r

#Setting Clock and Timer
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

#initial parameters
def init_bg():
    color=(0,0,255)
    randomlist=refreshpoints()
    x=400
    y=400
    r=15
    counter=0
    return color,randomlist,x,y,r,counter

color,randomlist,x,y,r,counter=init_bg()

running = True
gamerunning=True
while running:
    if gamerunning:
        text = str(counter)
        redraw(randomlist)
        screen.blit(font.render(text, True, (0, 0, 0)), (10, 10))
        randomlist,r=removepoints(x,y,r)
        
        #refresh points if points less than 100
        if len(randomlist)<100:
            randomlist=refreshpoints()

        #Creating and updating user blob
        pygame.draw.circle(screen, color,(int(x),int(y)), int(r))
        pygame.display.update()
        
        #Operation to be performed on key press(i.e moving the user Blob)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (x>50+r or (x>0+r and y>50+r)):
            x-=0.25
        elif keys[pygame.K_RIGHT] and x<width-r:
            x+=0.25
        elif keys[pygame.K_UP] and (y>50+r or (y>0+r and x>50+r)):
            y-=0.25
        elif keys[pygame.K_DOWN] and y<height-r:
            y+=0.25
            
        if counter==10:
            gamerunning=False
    else:
        font = pygame.font.SysFont('Consolas', 60)
        text="Game Over"
        screen.fill(background_colour)
        screen.blit(font.render(text, True, (0, 0, 0)), (250, 400))
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 
            counter += 1
        if event.type == pygame.QUIT:
            running = False
