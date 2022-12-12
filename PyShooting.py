import pygame
import sys
import random
import os
from time import sleep

padWidth = 480
padHeight = 640
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png'
            ,'rock06.png','rock07.png','rock08.png']

def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 물체의 개수' + str(count), True, (255,255,255))
    gamePad.blit(text,(10,0))

def writePassed(count):
    global gamepad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 물체' + str(count), True, (255,0,0))
    gamePad.blit(text,(360,0))

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('shooting')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, fighter, missile, explosion

    isShot = False
    shotCount = 0
    rockPassed = 0

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:
                    missileX = x + fighterWidth / 2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        drawObject(fighter, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]
            if bxy[1] < rockY:
                if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                    missileXY.remove(bxy)
                    isShot = True
                    shotCount += 1
                
                if bxy[1] < - 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0,padWidth - rockWidth)
            rockY = 0
            rockPassed += 1
        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY)

            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0,padWidth - rockWidth)
            rockY = 0
            isShot = False

            rockSpeed = random.randrange(1,7)
        
        drawObject(rock, rockX, rockY)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()