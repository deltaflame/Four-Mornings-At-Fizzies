import pygame, sys
import random as r
import os

from pygame.constants import KEYDOWN, K_a, K_d

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#four mornings at fizzys
map = []
directions = ["up", "down", "left", "right"]

pygame.init()
screen_width = 1920 // 2
screen_height = 1080 // 2
screen = pygame.display.set_mode((screen_width, screen_height))
powerPercent = 100

pepsoImage = pygame.image.load("pepso.png")
fantaImage = pygame.image.load("fanta.png")
backGround = pygame.image.load("fnaf background.png")
backGround = pygame.transform.scale(backGround, (screen_width * 1.4, screen_height))
#pepsoImage = pygame.transform.scale_by(pepsoImage, (0.75, 0.75))

animatronics = pygame.sprite.Group()

left_door_closed = False
right_door_closed = False

def toggleLeftDoor(doorClosed):
    if not doorClosed and not map[4][1]:
        map[4][1] = 'XX'
        return True
    elif doorClosed:
        map[4][1] = []
        return False

def toggleRightDoor(doorClosed):
    if not doorClosed and not map[4][3]:
        map[4][3] = 'XX'
        return True
    elif doorClosed:
        map[4][3] = []
        return False

def visualize():
    for row in map:
        for col in row:
            print(col, end = ' ')
        print()

for i in range(5):
    map.append([[], [], [], [], []])

map[3][1] = 'XX'
map[3][2] = 'XX'
map[3][3] = 'XX'

route1 = [(), (), (), (), (), (), (), ()]
route2 = []

guardPOV = 0

def moveCam(xPos):
    mouseX = pygame.mouse.get_pos()[0]
    if mouseX >= 0.9 * screen_width and xPos > screen_width * -0.4 + 160:
        return -40
    if mouseX <= 0.1 * screen_width and xPos < 0:
        return 40
    return 0

def checkWall(x, y, newX, newY):
    return map[x+newX][y+newY] != 'XX'

class atron(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(animatronics)
        self.x = x
        self.y = y
        self.name = name
        self.chance = 80
        self.timeSinceLastMoved = 0
    def __repr__(self):
        return self.name
    def move(self):
        direction = r.choice(directions)
        if r.randint(0,100) < 100 - self.chance:
            return
        match direction:
            case "up":
                if self.y > 0 and checkWall(self.x, self.y, 0, -1):
                    map[self.x][self.y].remove(self)
                    self.y -= 1
                    map[self.x][self.y].append(self)
            case "down":
                if self.y < 4 and checkWall(self.x, self.y, 0, 1):
                    map[self.x][self.y].remove(self)
                    self.y += 1
                    map[self.x][self.y].append(self)
            case "left":
                if self.x > 0 and checkWall(self.x, self.y, -1, 0):
                    map[self.x][self.y].remove(self)
                    self.x -= 1
                    map[self.x][self.y].append(self)
            case "right":
                if self.x < 4 and checkWall(self.x, self.y, 1, 0):
                    map[self.x][self.y].remove(self)
                    self.x += 1
                    map[self.x][self.y].append(self)
    def update(self):
        currTime = pygame.time.get_ticks()
        if currTime - self.timeSinceLastMoved >= 5000:
            self.timeSinceLastMoved = pygame.time.get_ticks()
            self.move()
            if self.name == 'f':
                self.move()

p = atron(0, 2, "p")
f = atron(0,2, "f")
map[4][2].append('G') 
map[p.x][p.y].append(p) 
map[f.x][f.y].append(f)
#p is for pepso
#f' #f is for fanti
#F # F is for fizzy
#c # c is for coca
#g #g is guard

class Button(pygame.sprite.Sprite):
    def __init__(self, size, pos, image):
        self.size = size
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(center = self.pos)
        self.toggle = False
        self.mouseDown = False
    def buttonClicked(self):
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not self.mouseDown:
                if self.rect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0]:
                    self.toggle = not self.toggle
                    self.mouseDown = True
                    print("clicked")
            if event.type == pygame.MOUSEBUTTONUP and self.mouseDown:
                self.mouseDown = False
                print("up")
    def draw(self):
        screen.blit(self.image, self.rect)
    def update(self):
        self.buttonClicked()
        self.draw()

test = Button(100, (screen_width // 2, 0), fantaImage)

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    #visualize()
    #print()
    #input()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                left_door_closed = toggleLeftDoor(left_door_closed)
            if event.key == K_d:
                right_door_closed = toggleRightDoor(right_door_closed)
            cls()
            visualize()
    animatronics.update()
    guardPOV += moveCam(guardPOV)
    screen.blit(backGround, (guardPOV,0))
    screen.blit(pepsoImage, (screen_width//2, screen_height//2))
    test.update()
    pygame.display.update()
        





























































































































































































