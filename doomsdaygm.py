import pygame

import os

import random

#Questions
#Why is the pass at the end of the enemy methods but not any other classes
#OOP vid
#Can't jump
#intialize the pygame
pygame.init()

#Screen 
Screenwid=500
Screenh=270
win = pygame.display.set_mode((Screenwid, Screenh))

#Title and Icon
pygame.display.set_caption('Doomsday: Out Of Time')

#Frame rate
clock= pygame.time.Clock()

#Score
global score
score = 0

#Sounds
bulletSound= pygame.mixer.Sound(open('C:\\Users\\18597\\Documents\\Coding\\My Python Scripts\\Doomsday\\Doomsday\\Pygame-Images (4)\\Game\\bull.wav'))
hitSound=pygame.mixer.Sound(open('C:\\Users\\18597\\Documents\\Coding\\My Python Scripts\\Doomsday\\Doomsday\\Pygame-Images (4)\\Game\\hit.wav'))
deathSound=pygame.mixer.Sound(open('C:\\Users\\18597\\Documents\\Coding\\My Python Scripts\\Doomsday\\Doomsday\\Pygame-Images (4)\\Game\\death.wav'))
music=pygame.mixer.music.load('bgMusic.mp3')
pygame.mixer.music.play(-1)

#Button Color to start
startButton=(0,0,51)
startButton2=(255,255,255)
#Button Text Color
textColor=(255,255,255)
textColor2=(0,0,51)
#Making a class for the player to clean up everything, OOP(Watch the Vid to understand)
class player(object):
    def __init__(self, x, y, width, height):
        #Atrrivutes of the Class
        self.x= x
        self.y= y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=7.5
        self.left=False
        self.right=False
        self.walkCount =0
        self.standing=True
        self.hitbox= (self.x +17, self.y+11, 29, 52)
        self.health=2
        self.alive=True
    def draw(self,win):
        if self.alive:
            #If we didn't cap the walkCount at 27, we would run out of images, or frames 9 images x 3 frames = 27
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                    self.walkCount+=1

                elif self.right:
                    win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                    self.walkCount +=1
            #We remove the stationary image to track which direction he was last looking at
            else:
                if self.right:
                    win.blit(walkRight[0],(self.x,self.y))
                else:
                    win.blit(walkLeft[0],(self.x, self.y))
            #Player Health Bar
            #Bar is green until players health goes down at which point the red is underneath the green bar and gets exposed.
            pygame.draw.rect(win,(255,0,0),(360,40,100,20))
            pygame.draw.rect(win,(0,255,0),(360,40, 100-((100/3)*(2- self.health)),20))
            #hit box of Luke
            self.hitbox= (self.x +17, self.y+11, 29, 52)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    def hit(self):
        if self.health>0:
            self.health -=1
            #Resets his postition
            self.x=230
            self.y=160
            self.walkCount=0
            #Adds a bit of delay so that the user knows what is going on
            i=0
            while i <100:
                pygame.time.delay(10)
                i += 10
                for event in pygame.event.get():
                    if event.type== pygame.QUIT:
                        i=301
                        pygame.quit()
        else:
            self.alive=False
            gameEnd()
        pass
        
        
        
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                     pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'),
                    pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        #x is where the nemey starts and end is where the enemy ends
        self.path= [self.x,self.end]
        self.walkCount = 0
        self.vel=3
        self.hitbox= (self.x +17, self.y+2, 31, 57)
        self.health=2
        self.alive=True
        
    def draw(self,win):
        self.move()
        if self.alive:
            if self.walkCount +1 <= 33:
                self.walkCount=0
            if self.vel >0:
                win.blit(self.walkRight[self.walkCount //3], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x,self.y))
                self.walkCount += 1
                    
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0], self.hitbox[1]-20, 50,10))
            pygame.draw.rect(win,(0,255,0),(self.hitbox[0], self.hitbox[1]-20, 50-((50/3)*(2- self.health)),10))
            #The hitbox of enemy
            self.hitbox= (self.x +20, self.y, 28, 60)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel>0:
            #the 1 is end becuase lists go from 0
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel *-1
                self.walkCount=0
        else:
            if self.x-self.vel>self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel *-1
                self.walkCount=0
        pass
    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            global score
            score +=1
            if score==10:
                gameWon()
            self.x=random.randint(70,430)
            self.health=2
            pass
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x =x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        #Facing will either be -1 or 1, determining which diraction the bullet goes in.
        self.vel= 8*facing
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

#Character Animation
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'),
                 pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'),
                pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('cityimage.png')
char = pygame.image.load('standing.png')

#Button for Start
def button(msg,x,y,w,h,inactive,active,xT,yT,inactiveT,activeT,action=None):
        #Use location of mouse to track the button
        mouse= pygame.mouse.get_pos()
        #Tracks mouse clicks
        click=pygame.mouse.get_pressed() 
        #0 is x, 1 is y, 2 is width, 3 is height
        if x+w> mouse[0] >x and y+h>mouse[1]>y:
            pygame.draw.rect(win, inactive,(x,y,w,h))
            #Click[0] is left mouse click
            if click[0] == 1 and action!= None:
                if action == 'play':
                    gameLoop()
        else:       
            pygame.draw.rect(win, active,(x,y,w,h))

        buttonText= pygame.font.SysFont('goudystout',15,False,False)
        buttonType= buttonText.render(msg,1,(activeT))
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))
        if x+w> mouse[0] >x and y+h>mouse[1] > y:
            win.blit(buttonType2,(xT,yT))
        else:
            win.blit(buttonType,(xT,yT))            
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))

#Button for Directions
def buttonDir(msg,x,y,w,h,inactive,active,xT,yT,inactiveT,activeT,action=None):
        #Use location of mouse to track the button
        mouse= pygame.mouse.get_pos()
        #Tracks mouse clicks
        click=pygame.mouse.get_pressed() 
        #0 is x, 1 is y, 2 is width, 3 is height
        if x+w> mouse[0] >x and y+h>mouse[1]>y:
            pygame.draw.rect(win, inactive,(x,y,w,h))
            #Click[0] is left mouse click
            if click[0] == 1 and action!= None:
                if action == 'directions':
                    dirPage()
        else:       
            pygame.draw.rect(win, active,(x,y,w,h))

        buttonText= pygame.font.SysFont('goudystout',15,False,False)
        buttonType= buttonText.render(msg,1,(activeT))
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))
        if x+w> mouse[0] >x and y+h>mouse[1] > y:
            win.blit(buttonType2,(xT,yT))
        else:
            win.blit(buttonType,(xT,yT))            
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))

def backButton(msg,x,y,w,h,inactive,active,xT,yT,inactiveT,activeT,action=None):
        #Use location of mouse to track the button
        mouse= pygame.mouse.get_pos()
        #Tracks mouse clicks
        click=pygame.mouse.get_pressed() 
        #0 is x, 1 is y, 2 is width, 3 is height
        if x+w> mouse[0] >x and y+h>mouse[1]>y:
            pygame.draw.rect(win, inactive,(x,y,w,h))
            #Click[0] is left mouse click
            if click[0] == 1 and action!= None:
                if action == 'dirPage':
                    dirPage()
        else:       
            pygame.draw.rect(win, active,(x,y,w,h))

        buttonText= pygame.font.SysFont('goudystout',15,False,False)
        buttonType= buttonText.render(msg,1,(activeT))
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))
        if x+w> mouse[0] >x and y+h>mouse[1] > y:
            win.blit(buttonType2,(xT,yT))
        else:
            win.blit(buttonType,(xT,yT))            
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))
        
def forButton(msg,x,y,w,h,inactive,active,xT,yT,inactiveT,activeT,action=None):
        #Use location of mouse to track the button
        mouse= pygame.mouse.get_pos()
        #Tracks mouse clicks
        click=pygame.mouse.get_pressed() 
        #0 is x, 1 is y, 2 is width, 3 is height
        if x+w> mouse[0] >x and y+h>mouse[1]>y:
            pygame.draw.rect(win, inactive,(x,y,w,h))
            #Click[0] is left mouse click
            if click[0] == 1 and action!= None:
                if action == 'dirPage2':
                    dirPage2()
        else:       
            pygame.draw.rect(win, active,(x,y,w,h))

        buttonText= pygame.font.SysFont('goudystout',15,False,False)
        buttonType= buttonText.render(msg,1,(activeT))
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))
        if x+w> mouse[0] >x and y+h>mouse[1] > y:
            win.blit(buttonType2,(xT,yT))
        else:
            win.blit(buttonType,(xT,yT))            
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))

def backButtonStart(msg,x,y,w,h,inactive,active,xT,yT,inactiveT,activeT,action=None):
        #Use location of mouse to track the button
        mouse= pygame.mouse.get_pos()
        #Tracks mouse clicks
        click=pygame.mouse.get_pressed() 
        #0 is x, 1 is y, 2 is width, 3 is height
        if x+w> mouse[0] >x and y+h>mouse[1]>y:
            pygame.draw.rect(win, inactive,(x,y,w,h))
            #Click[0] is left mouse click
            if click[0] == 1 and action!= None:
                if action == 'start':
                    start()
        else:       
            pygame.draw.rect(win, active,(x,y,w,h))

        buttonText= pygame.font.SysFont('goudystout',15,False,False)
        buttonType= buttonText.render(msg,1,(activeT))
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))
        if x+w> mouse[0] >x and y+h>mouse[1] > y:
            win.blit(buttonType2,(xT,yT))
        else:
            win.blit(buttonType,(xT,yT))            
        buttonText2= pygame.font.SysFont('goudystout',15,False,False)
        buttonType2= buttonText2.render(msg,1,(inactiveT))

def dirPage():
    direct=True
    while direct:
        #To mkae the start screen go away
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg,(0,0))
        dirText=pygame.font.SysFont('goudystout',15,True,False)
        dirGame=dirText.render('Help Luke deliver Tobias', 1, (255,255,255))
        win.blit(dirGame,(30,30))
        dirText2=pygame.font.SysFont('goudystout',15,True,False)
        dirGame2=dirText2.render('to the Release Station', 1, (255,255,255))
        win.blit(dirGame2,(45,80))
        dirText3=pygame.font.SysFont('goudystout',15,True,False)
        dirGame3=dirText3.render('Elminate 10 Guards to get', 1, (255,255,255))
        win.blit(dirGame3,(20,130))
        dirText35=pygame.font.SysFont('goudystout',15,True,False)
        dirGame35=dirText35.render(' to the Release Station', 1, (255,255,255))
        win.blit(dirGame35,(45,170))

        forButton('Next',330,220,100,45,startButton2,startButton,345,230,textColor2,textColor,'dirPage2')
        backButtonStart('Back',30,220,100,45,startButton2,startButton,45,230,textColor2,textColor,'start')
        
        pygame.display.update()
        clock.tick(15)

def dirPage2():
    direct2=True
    while direct2:
        #To mkae the start screen go away
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg,(0,0))
        dirText4=pygame.font.SysFont('goudystout',12,True,False)
        dirGame4=dirText4.render('Use the left and right arrow keys', 1, (255,255,255))
        win.blit(dirGame4,(10,30))
        dirText45=pygame.font.SysFont('goudystout',15,True,False)
        dirGame45=dirText45.render('to move', 1, (255,255,255))
        win.blit(dirGame45,(170,60))
        dirText5=pygame.font.SysFont('goudystout',12,True,False)
        dirGame5=dirText5.render('Shoot your gun with the space bar', 1, (255,255,255))
        win.blit(dirGame5,(10,105))
        dirText6=pygame.font.SysFont('goudystout',11,True,False)
        dirGame6=dirText6.render('If you get hit by guards three times', 1, (255,255,255))
        win.blit(dirGame6,(10,140))
        dirText65=pygame.font.SysFont('goudystout',15,True,False)
        dirGame65=dirText65.render('You will die', 1, (255,255,255))
        win.blit(dirGame65,(150,175))


        backButton('Back',200,220,100,45,startButton2,startButton,215,235,textColor2,textColor,'dirPage')
        
        pygame.display.update()
        clock.tick(15)
#Starting Screen text
def start():
    intro=True
    while intro:
        #To mkae the start screen go away
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg,(0,0))
        startText=pygame.font.SysFont('goudystout',30,True,False)
        startGame= startText.render('Doomsday', 1, (255,255,255))
        win.blit(startGame,(90,90))
        startText2=pygame.font.SysFont('goudystout',30,True,False)
        startGame2= startText2.render('Out Of Time', 1, (255,255,255))
        win.blit(startGame2,(60,150))
        
        button('Start',30,190,180,50,startButton2,startButton,75,205,textColor2,textColor,'play')
        buttonDir('Directions',280,190,200,50,startButton2,startButton,300,205,textColor2,textColor,'directions')
        
        pygame.display.update()
        clock.tick(15)

def gameEnd():
    end=True
    while end:
        #To mkae the start screen go away
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()                    
                quit()
        win.blit(bg,(0,0))
        endText=pygame.font.SysFont('goudystout',30,True,False)
        endGame=endText.render('GAME OVER',1,(255,255,255))
        win.blit(endGame,(90,110))
                          
        backButtonStart('Play Again',165,190,200,50,startButton2,startButton,180,205,textColor2,textColor,'start')
        
        pygame.display.update()
        clock.tick(15)

def gameWon():
    won=True
    while won:
        #To mkae the start screen go away
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg,(0,0))
        wonText=pygame.font.SysFont('goudystout',20,True,False)
        wonGame=wonText.render('Congratulations!',1,(255,255,255))
        win.blit(wonGame,(60,60))
        wonText2=pygame.font.SysFont('goudystout',15,True,False)
        wonGame2=wonText2.render('You delivered Tobias to',1,(255,255,255))
        win.blit(wonGame2,(60,105))
        wonText25=pygame.font.SysFont('goudystout',15,True,False)
        wonGame25=wonText25.render('the Release Station',1,(255,255,255))
        win.blit(wonGame25,(75,150))
        

        backButtonStart('Play Again',165,190,200,50,startButton2,startButton,180,205,textColor2,textColor,'start')

        pygame.display.update()
        clock.tick()

def redrawGameWindow():
    win.blit(bg,(0,0))
    text= font.render('Score: ' +str(score), 1, (255,255,255))
    win.blit(text,(350,10))
    Luke.draw(win)
    soldier.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()
    
def gameLoop():

    #Game Loop
    #Font, (Font, Size, Bold, Italisize
    global font
    font= pygame.font.SysFont('goudystout', 15, True, False)
    #Luke is an instace of the player class
    #player(parameters)
    global Luke
    Luke= player(230,160,64,64)
    global soldier
    soldier =enemy(130,165,64,64,200)
    run=True
    global bullets
    bullets= []
    shootLoop = 0
    #this make the game start when any key is pressed
    while run:
                clock.tick(27)
                if soldier.alive:
                        if Luke.hitbox[1] <soldier.hitbox[1] + soldier.hitbox[3] and soldier.hitbox[3] and Luke.hitbox[1] + Luke.hitbox[3] > soldier.hitbox[1]:
                            if Luke.hitbox[0] + Luke.hitbox[2]  > soldier.hitbox[0]   and Luke.hitbox[0]  < soldier.hitbox[0] + soldier.hitbox[2]:
                                Luke.hit()
                                deathSound.play()
            #Shoot Loop is to shoot 1 bullet at a time not 2 or 3
                if shootLoop >0:
                    shootLoop +=1
                if shootLoop >3:
                     shootLoop =0
                pygame.time.delay(100)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run=False
                for bullet in bullets:
                    if soldier.alive:
                        #We check for collision by checking if the bullet is in the same y and x corridate as the enemy 0 is x for soldier and 1 is the y corridnate, 3 is height and 2 is width
                        if bullet.y  - bullet.radius <soldier.hitbox[1] + soldier.hitbox[3] and soldier.hitbox[3] and bullet.y + bullet.radius > soldier.hitbox[1]:
                            if bullet.x + bullet.radius > soldier.hitbox[0]   and bullet.x - bullet.radius < soldier.hitbox[0] + soldier.hitbox[2]:
                                hitSound.play()
                                soldier.hit()
                                bullets.pop(bullets.index(bullet))
                    if bullet.x < 500 and bullet.x > 0:
                        bullet.x += bullet.vel
                    else:
                        bullets.pop(bullets.index(bullet))         
                #We have to put Luke._ because it is an attribute of the class now not just a variable
                keys=pygame.key.get_pressed()

                if keys[pygame.K_SPACE] and shootLoop == 0:
                    if Luke.left:
                        facing = -1
                    else:
                        facing = 1
                    if len(bullets) < 4:
                        bulletSound.play()
                        bullets.append(projectile(round(Luke.x+Luke.width //2 ), round(Luke.y +Luke.height//2), 6, (176,141,87),facing))
                    shootLoop=1
                if keys[pygame.K_LEFT] and Luke.x >  Luke.vel:
                    Luke.x -= Luke.vel
                    Luke.left= True
                    Luke.right=False
                    Luke.standing= False
                elif keys[pygame.K_RIGHT] and Luke.x < Screenwid -  Luke.width-  Luke.vel:
                     Luke.x += Luke.vel
                     Luke.left=False
                     Luke.right=True
                     Luke.standing=False

                     Luke.walkCount=0
                if not( Luke.isJump):
                    if keys[pygame.K_w]:
                         Luke.isJump=True
                         Luke.left=False
                         Luke.right=False
                         Luke.walkcount=0 
                else:
                    #If the jump is at its orginal state
                    if  Luke.jumpCount >= -7.5:
                        neg = 1
                        #neg makes it go down after the Apex
                        if  Luke.jumpCount < 0:
                            #When the jump is at its Apex, neg impacts the Jump Count by making it go down
                            neg= -1
                        #The y is decreased so the character goes up, increases 100p,90p, going down by 10.
                            Luke.y -=  Luke.jumpCount ** 2 //2 * neg
                            Luke.jumpCount -= 1

                    else:
                         Luke.isJump= False
                         Luke.jumpCount=7.5
                redrawGameWindow()
start()
pygame.quit()
