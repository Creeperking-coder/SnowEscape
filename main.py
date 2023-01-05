import pygame
import random

pygame.init()

windowwidth = 800
windowheight = 800

win = pygame.display.set_mode((windowwidth, windowheight))
black = (0, 0, 0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grey = (129,126,130)
dark_grey = (69,66,70)
brown = (25,12,2)
yellow = (250,250,0)

class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.width = 18
        self.height = 25
        self.speed = 1
        self.xvel = 0
        self.yvel = 0
        self.pvelx = 1
        self.pvely = 1
        self.stickDoll = False
        self.photograph = False
        self.book = False
        self.lampx = self.x + 5 + self.xvel * 10
        self.lampy = self.y - 5
        self.range = 15
        self.img = pygame.image.load("Player.png")
        self.img2 = pygame.image.load("Playerflip.png")
        self.img3 = pygame.image.load("Playerup.png")
        self.img4 = pygame.image.load("Playerup2.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.img2 = pygame.transform.scale(self.img2, (self.width, self.height))
        self.img3 = pygame.transform.scale(self.img3, (self.width, self.height))
        self.img4 = pygame.transform.scale(self.img4, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lamprect = pygame.Rect(self.lampx-self.range,self.lampy-self.range,self.range*2,self.range*2)
    def tick(self, win):

        self.x += self.xvel * self.speed
        self.y += self.yvel * self.speed

        if self.x < 20:
            self.x = 20
        elif self.x > 780-self.width:
            self.x = 780-self.width
        if self.y < 20:
            self.y = 20
        elif self.y > 780-self.height:
            self.y = 780-self.height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.lampx = self.x + self.width/2
        self.lampy = self.y + self.height/2

        if self.pvelx > 0:
            self.lampx = self.x + 17
        elif self.pvelx < 0:
            self.lampx = self.x
        if self.pvely > 0:
            self.lampy = self.y + 17
        elif self.pvely < 0:
            self.lampy = self.y + 7


        self.lamprect = pygame.Rect(self.lampx-self.range,self.lampy-self.range,self.range*2,self.range*2)
        pygame.draw.circle(win,yellow,(self.lampx,self.lampy),self.range)
        if self.pvelx > 0:
            if self.pvely != 0:
                win.blit(self.img3, self.rect)
            else:
                win.blit(self.img,self.rect)
        elif self.pvelx < 0:
            if self.pvely != 0:
                win.blit(self.img4, self.rect)
            else:
                win.blit(self.img2, self.rect)

class Buttons:
    def __init__(self):
        self.x = -200
        self.y = -200
        self.width = 30
        self.height = 45
        self.img = pygame.image.load("Buttons.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.state = "attack"
        self.timer = 0
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def tick(self, win):

        if self.state == "docile":
            self.timer += random.randint(0,2)
            if self.timer >= 400:
                if random.randint(0,1) == 0:
                    self.state = "attack"
                self.timer = 0
        elif self.state == "attack":

            if player.x - self.x > 2:
                self.x += self.speed
            elif player.x - self.x < -2:
                self.x -= self.speed
            if player.y - self.y > 2:
                self.y += self.speed
            elif player.y - self.y < -2:
                self.y -= self.speed

            if self.rect.colliderect(player.rect) == True:
                return False
            elif self.rect.colliderect(player.lamprect) == True:
                self.state = "flee"
                for i in range(50):
                    s = Snow()
        elif self.state == "flee":
            self.pos = pygame.Vector2(self.x, self.y)
            self.x, self.y = pygame.Vector2.lerp(self.pos, pygame.Vector2(-200,200), 0.1)

            if self.x < 0 and self.y > 0:
                self.state = "docile"
                self.x = random.choice([1000,-200])
                self.y = random.choice([1000,-200])


        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(self.img,self.rect)
        return True

class Smiler:
    smilers = []
    def __init__(self):
        self.x = random.randint(100,700)
        self.y = random.randint(100,700)
        self.width = 13
        self.height = 15
        self.img = pygame.image.load("Smiler.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.state = "attack"
        self.stage = 0
        self.timer = 0
        self.flicker = 0
        self.flickermax = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        Smiler.smilers.append(self)
    def tick(self, win):

        if self.state == "docile":
            self.timer += random.randint(0,2)
            if self.timer >= 1000:
                self.state = "attack"
                self.timer = 0

        elif self.state == "attack":
            self.timer += random.randint(0,2)
            if self.timer >= 400:
                self.stage += 1
                self.timer = 0
                self.x = random.randint(100, 700)
                self.y = random.randint(100, 700)
            if self.rect.colliderect(player.lamprect) == True:
                self.stage -= 1
                if self.stage <= 0:
                    self.state = "docile"
                    self.timer = 0


        if self.stage >= 5:
            return False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.flickermax = 1
        if self.stage == 1:
            self.flickermax = 20
        elif self.stage == 2:
            self.flickermax = 10
        elif self.stage == 3:
            self.flickermax = 5
        elif self.stage == 4:
            self.flickermax = 3


        self.flicker += 1
        if self.flicker >= self.flickermax:
            self.flicker = 0
            win.blit(self.img,self.rect)
        return True

class Snow:
    snowflakes = []
    def __init__(self):
        self.x = random.randint(0,800)
        self.y = random.randint(0,800)
        self.width = 10
        self.height = 10
        self.speed = random.randint(2,5)
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        Snow.snowflakes.append(self)
    def tick(self,win):

        if self.x <= 0:
            self.x += 800
        if self.y >= 800:
            self.y -= 800

        self.x -= self.speed
        self.y += self.speed

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win,white,self.rect)

class Tree:
    trees = []
    def __init__(self,area,x,y):
        self.x = x
        self.y = y
        self.width = 96
        self.height = 96
        self.area = area
        self.img = pygame.image.load("Tree.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        Tree.trees.append(self)
    def tick(self,win):

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(self.img,self.rect)

class transfer:
    transfers = []
    def __init__(self,x,y,width,height,a,na):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.area = a
        self.next_area = na
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        transfer.transfers.append(self)
    def tick(self, win):


        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win,dark_grey,self.rect)

class Prop:
    props = []
    def __init__(self,area,x,y,image,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.area = area
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        Prop.props.append(self)
    def tick(self,win):

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(self.img,self.rect)

class Artifact:
    artifacts = []
    def __init__(self,area,x,y,image,width,height,type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.area = area
        self.type = type
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        Artifact.artifacts.append(self)
    def tick(self,win):

        if player.rect.colliderect(self.rect) == True:
            if self.type == "stickdoll":
                player.stickDoll = True
                s = Sticks()
            elif self.type == "photograph":
                player.photograph = True
                s = Smiler()
            elif self.type == "book":
                player.book = True
                d = Dream()
            Artifact.artifacts.remove(self)
            return

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(self.img,self.rect)

for i in range(50):
    l = Snow()
for i in range(10):
    t = Tree(0, random.randint(20, 680), random.randint(20, 680))
    t = Tree(9, random.randint(20, 300), random.randint(20, 680))
    t = Tree(9, random.randint(500, 680), random.randint(20, 680))
for i in range(15):
    t = Tree(1, random.randint(20, 680), random.randint(20, 680))
for i in range(20):
    t = Tree(2, random.randint(20, 680), random.randint(20, 680))
    t = Tree(3, random.randint(20, 680), random.randint(20, 680))
    t = Tree(5, random.randint(20, 680), random.randint(20, 680))
    t = Tree(6, random.randint(20, 680), random.randint(20, 680))

t = Tree(7, 400-96/2, 400-96/2)
t = Tree(7, 400-96/2, 600-96/2)
t = Tree(7, 500-96/2, 500-96/2)
t = Tree(7, 300-96/2, 500-96/2)
t = Tree(7, 200-96/2, 200-96/2)
t = Tree(7, 600-96/2, 200-96/2)

t = Tree(10,400,500)
t = Tree(10,280,450)
t = Tree(10,200,350)
t = Tree(10,290,240)
t = Tree(10,400,200)
t = Tree(10,500,300)
t = Tree(10,400,360)

#props
p = Artifact(7,400,500,"TwigDoll.png",13,15,"stickdoll")
p = Artifact(10,400,400,"Book.png",22,20,"book")
p = Artifact(4,400,400,"Photograph.png",21,19,"photograph")

player = Player()

#transfers to other areas
t = transfer(400,0,100,50,0,1)
t = transfer(400,0,100,50,1,0)

t = transfer(0,400,50,100,1,2)
t = transfer(0,400,50,100,2,1)

t = transfer(200,750,100,50,2,3)
t = transfer(200,750,100,50,3,2)

t = transfer(500,0,100,50,2,4)
t = transfer(500,0,100,50,4,2)

t = transfer(500,0,100,50,3,5)
t = transfer(500,0,100,50,5,3)

t = transfer(750,100,50,100,5,6)
t = transfer(750,100,50,100,6,5)

t = transfer(750,250,50,100,5,7)
t = transfer(750,250,50,100,7,5)

t = transfer(750,400,50,100,5,8)
t = transfer(750,400,50,100,8,5)

t = transfer(0,400,50,100,6,9)
t = transfer(0,400,50,100,9,6)

t = transfer(750,400,50,100,9,10)
t = transfer(750,400,50,100,10,9)

t = transfer(400,0,100,50,9,11)
t = transfer(400,0,100,50,11,9)

p = Prop(9,400,0,"road.png",100,800)
p = Prop(11,400,0,"road.png",100,800)

button = Buttons()

area = 11
run = True

while run == True:

    pygame.time.delay(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    win.fill(brown)

    for t in Tree.trees:
        if area == t.area:
            t.tick(win)

    for p in Prop.props:
        if area == p.area:
            p.tick(win)

    for m in transfer.transfers:
        if m.area == area:
            m.tick(win)
            if m.rect.colliderect(player.rect) == True:
                area = m.next_area
                for i in Smiler.smilers:
                    i.stage = 0
                player.x -= (m.x+m.width/2 - player.x)
                player.y -= (m.y+m.height/2 - player.y)
                player.tick(win)

    player.tick(win)

    for a in Artifact.artifacts:
        if area == a.area:
            a.tick(win)

    run = button.tick(win)
    for i in Smiler.smilers:
        run = i.tick(win)

    for i in Snow.snowflakes:
        i.tick(win)

    #snowflake limit
    if len(Snow.snowflakes)>400:
        Snow.snowflakes.remove(Snow.snowflakes[-1])

    player.yvel = 0
    player.xvel = 0
    if keys[pygame.K_w] == True:
        player.yvel = -1
        player.pvely = -1
    elif keys[pygame.K_s] == True:
        player.yvel = 1
        player.pvely = 1
    if keys[pygame.K_d] == True:
        player.xvel = 1
        player.pvelx = 1
        player.pvely = 0
    elif keys[pygame.K_a] == True:
        player.xvel = -1
        player.pvelx = -1
        player.pvely = 0

    pygame.draw.rect(win, black, (0, 0, 800, 800), 20)

    pygame.display.update()









