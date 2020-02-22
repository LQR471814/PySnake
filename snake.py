import pygame
from pygame.locals import *
import time
import sys
import threading
import random

class apple:
    def __init__(self, location, pointValue):
        self.location = location
        self.pointValue = pointValue

    def updateSelf(self):
        global screen
        global increment
        drawBlock((self.location[0] * increment, self.location[1] * increment), (255, 0, 0))

class snake:
    def __init__(self, location, direction):
        self.location = location
        self.direction = direction

    def move(self):
        global increment
        global tickSpeed
        global screen

        # for i in range(increment): #* Dead attempt at making the snake move smoothly (I didn't want to complete it)
        #     time.sleep(tickSpeed / increment)

        #     tmpLocale = []
        #     tmpLocale.append(self.location[0] * increment + 1 * self.direction[0])
        #     tmpLocale.append(self.location[1] * increment + 1 * self.direction[1])

        #     self.location = tmpLocale

        #     drawBlock(self.location, (255, 255, 255))

        # newLocale.append(tmpLocale[0] / increment)
        # newLocale.append(tmpLocale[1] / increment)
        # self.location = newLocale

        #? Tip because I spent around 30 minutes debugging this stupid thing:
        #? The newLocale list variable is used instead of individually assigning items in the list location attribute because doing so would cause pythonic "Black Magic" (It would make things really weird and set list variables to something else)

        newLocale = []
        newLocale.append(self.location[0] + self.direction[0] * 1)
        newLocale.append(self.location[1] + self.direction[1] * 1)
        self.location = newLocale
        self.updateSelf()

    def updateSelf(self):
        global screen
        drawBlock((self.location[0] * increment, self.location[1] * increment), (255, 255, 255))

def drawBlock(TopLeftLocation, color):
    global increment
    global screen
    pygame.draw.rect(screen, color, pygame.Rect(TopLeftLocation[0], TopLeftLocation[1], increment, increment))

def checkForCollisionSelf():
    global snakeList
    global tickSpeed
    global stopMovement
    while True:
        time.sleep(tickSpeed / 2)
        x = 0
        for snakeObj in snakeList:
            if x != 0:
                if snakeObj.location == snakeList[0].location:
                    stopMovement = True
            x += 1

def checkForCollisionApple():
    global snakeList
    global appleObj
    global snakeLength
    global tickSpeed
    while True:
        time.sleep(tickSpeed / 2)
        if snakeList[0].location == appleObj.location:
            for i in range(appleObj.pointValue):
                snakeList.insert(0, snake(snakeList[0].location, snakeList[0].direction))
                snakeList[0].updateSelf()
                snakeList[0].move()
            appleObj = apple( [ random.randint(0, int(screensize[0] / increment) - 1), random.randint(0, int(screensize[1] / increment) - 1) ], 1)
            snakeLength += 1

def checkForCollisionWall():
    global snakeList
    global stopMovement
    global screensize
    global tickSpeed
    while True:
        time.sleep(tickSpeed / 2)
        if snakeList[0].location[0] < 0:
            stopMovement = True
            return

        if snakeList[0].location[1] < 0:
            stopMovement = True

        if snakeList[0].location[0] >= screensize[0] / increment:
            stopMovement = True

        if snakeList[0].location[1] >= screensize[1] / increment:
            stopMovement = True

def keepTheSnakeMoving():
    global snakeList
    global tickSpeed
    global stopMovement
    while True:

        if stopMovement == True:
            return

        time.sleep(tickSpeed)
        snakeList.insert(0, snake(snakeList[0].location, snakeList[0].direction))
        snakeList.pop(len(snakeList) - 1)
        snakeList[0].move()
        snakeList[0].updateSelf()

#? Settings
screensize = [600, 600] #? Screensize (Does not need to be square)
increment = 25 #? Game scale (In pixels)

#? Advanced Settings
tickSpeed = 0.1 #? How fast should the game run? (The lower the number is, the faster)
inputDelay = 0.005 #? How much input delay should there be? (Not actual input delay but sort of similar)
snakeLength = 0 #? Starting score value
snakeList = [snake([0, 0], [1, 0]), snake([0, 1], [1, 0]), snake([0, 2], [1, 0])] #? The list of snake bodies and snake head (The distinction is whichever snake object is at index 0 then it is the "head") You can add more objects in the intial list to make the snake longer initially
appleObj = apple( [ random.randint(0, int(screensize[0] / increment)) - 1, random.randint(0, int(screensize[1] / increment)) - 1 ], 1) #? Constructs the initial object "apple", you can modify the construct parameters and change where the initial apple will spawn and how much it will be worth (If you wish to change the other apples construct parameters go to line 86)
stopMovement = False #? Turn this to true if you wish to lose the game right from the start

pygame.init()
screen = pygame.display.set_mode(screensize)

#? Checks for collision with self
selfCollisionThread = threading.Thread(target=checkForCollisionSelf)
selfCollisionThread.daemon = True
selfCollisionThread.start() #? Comment this line out to disable self collision!

#? Check for collision with apple
appleCollisionThread = threading.Thread(target=checkForCollisionApple)
appleCollisionThread.daemon = True
appleCollisionThread.start() #? Comment this line out to disable apple collision!

#? Check for collision with wall
wallCollisionThread = threading.Thread(target=checkForCollisionWall)
wallCollisionThread.daemon = True
wallCollisionThread.start() #? Comment this line out to disable wall collision!

#? Allows the snake to keep moving
movementThread = threading.Thread(target=keepTheSnakeMoving)
movementThread.daemon = True
movementThread.start() #? Comment this line out to disable snake movement!

while True:
    screen.fill((0, 0, 0))
    keystate = pygame.key.get_pressed()

    if stopMovement == True:
        break

    if keystate[pygame.K_ESCAPE]:
        stop = True
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == QUIT:
            stop = True
            pygame.quit()
            sys.exit()

    if keystate[pygame.K_RIGHT]:
        if snakeList[0].direction != [-1, 0]:
            snakeList[0].direction = [1, 0]

    if keystate[pygame.K_LEFT]:
        if snakeList[0].direction != [1, 0]:
            snakeList[0].direction = [-1, 0]

    if keystate[pygame.K_UP]:
        if snakeList[0].direction != [0, 1]:
            snakeList[0].direction = [0, -1]

    if keystate[pygame.K_DOWN]:
        if snakeList[0].direction != [0, -1]:
            snakeList[0].direction = [0, 1]

    for snakeObj in snakeList:
        snakeObj.updateSelf()

    appleObj.updateSelf()

    pygame.display.update()
    time.sleep(inputDelay)

print("Your score is: " + str(snakeLength))