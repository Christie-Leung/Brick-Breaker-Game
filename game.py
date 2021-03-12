"""
Title: Brick Breaker Game Engine
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame

from bricks import Brick
from imageSprite import ImageSprite
from loader import Color, Image
from text import Text
from window import Window
from random import randrange
from coin import Coin


class Game:
    pygame.init()
    def __init__(self):
        ## Setup
        self.WINDOW = Window()
        self.WINDOW.setBackgroundImage(Image.BACKGROUND)
        self.TITLE = ImageSprite(Image.TITLE)
        self.TITLE.setPOS((self.WINDOW.getVirtualWidth()-self.TITLE.getWidth())//2, 50)

        self.STARTGAME = False
        self.MENU = True

        # Ball
        self.BALL = ImageSprite(Image.WRECKITRALPH)
        self.BALL.setScale(14)
        # Paddle
        self.PLAYER = Brick(Image.PLAYER)
        self.PLAYER.setScale(8)
        self.PLAYER.setSpeed(8)

        #Difficulty
        self.EASY_IMG = ImageSprite(Image.EASY)
        self.EASY_IMG.setScale(2)
        self.EASY_IMG.setPOS((self.WINDOW.getVirtualWidth()-self.EASY_IMG.getWidth())//2,
                             7*(2*self.WINDOW.getVirtualHeight()//3 - self.EASY_IMG.getHeight())//8)
        self.MED_IMG = ImageSprite(Image.MED)
        self.MED_IMG.setScale(2)
        self.MED_IMG.setPOS((self.WINDOW.getVirtualWidth() - self.MED_IMG.getWidth()) // 2,
                             self.EASY_IMG.getY() + self.EASY_IMG.getHeight() + 5)
        self.HARD_IMG = ImageSprite(Image.HARD)
        self.HARD_IMG.setScale(2)
        self.HARD_IMG.setPOS((self.WINDOW.getVirtualWidth() - self.HARD_IMG.getWidth()) // 2,
                             self.MED_IMG.getY() + self.MED_IMG.getHeight() + 5)
        self.DIFFICULTY = 0

        # Lives
        self.LIVES = []

        # Bricks
        self.TEMPLATE = ImageSprite(Image.BRICKS[0])
        self.TEMPLATE.setScale(5)
        self.BRICKS = []

        # Brick Collision
        self.COLLISION_MS = 0
        self.COLLISION_TIMER = pygame.time.Clock()
        self.COLLISION = False
        self.X_COLLISION = -5
        self.Y_COLLISION = -5

        # Coins
        self.COINS = []
        self.SCORE = 0
        self.COINS_TXT = Text(f"Coins: {self.SCORE}")

        # Game Over
        self.GAME_OVER_TXT = Text("Game Over!")
        self.GAME_OVER = False
        self.GAME_OVER_TXT.setFontSize(50)
        self.GAME_OVER_TXT.setPOS((self.WINDOW.getVirtualWidth()-self.GAME_OVER_TXT.getWidth())//2, (self.WINDOW.getVirtualHeight()-self.GAME_OVER_TXT.getHeight())//2)

    def initiateStartMenu(self):
        self.WINDOW.clearScreen()
        self.updateCoins()
        self.blit(self.COINS_TXT)
        self.blit(self.TITLE)
        self.blit(self.EASY_IMG)
        self.blit(self.MED_IMG)
        self.blit(self.HARD_IMG)

    def initiateBricks(self, levels):
        # Place bricks on screen
        self.BRICKS.clear()
        self.COINS.clear()
        X = 55
        X_PADDING = 20
        Y = 40
        for i in range(levels):
            WIDTHLEFT = self.WINDOW.getVirtualWidth() - (2*X_PADDING)
            SPACE = 5
            BRICK_WIDTH = self.TEMPLATE.getWidth()
            if (i+1) % 2 == 0:
                WIDTHLEFT -= BRICK_WIDTH
            while WIDTHLEFT - BRICK_WIDTH > 0:
                WIDTHLEFT -= BRICK_WIDTH + SPACE
                BRICK = Brick(Image.BRICKS[0])
                BRICK.setScale(5)
                BRICK.setPOS(X, Y)
                X += BRICK_WIDTH + SPACE
                self.BRICKS.append(BRICK)
                BRICK.updateWalls(self.WINDOW.getScreen())
                self.blit(BRICK)
            if i % 2 == 0:
                X = 55 + BRICK_WIDTH//2
            else:
                X = 55
            Y += SPACE + self.TEMPLATE.getHeight()
        self.blit(self.BALL)
        self.blit(self.PLAYER)
        self.WINDOW.updateFrame()

    def initiateLevel(self):
        if self.DIFFICULTY == 1:
            self.initiateBricks(3)
            self.BALL.setSpeed(4)
        if self.DIFFICULTY == 2:
            self.initiateBricks(4)
            self.BALL.setSpeed(8)
        if self.DIFFICULTY == 3:
            self.initiateBricks(5)
            self.BALL.setSpeed(12)

    def getSpriteCollision(self, SPRITE, SPRITE2):
        try:
            if pygame.Rect.colliderect(SPRITE.getRect(), SPRITE2.getRect()):
                return True
            else:
                return False
        except AttributeError:
            if pygame.Rect.colliderect(SPRITE, SPRITE2.getRect()):
                return True
            else:
                return False

    def startGame(self, lives):
        self.GAME_OVER = False
        self.MENU = False
        SPACING = 0
        self.BALL.setPOS((self.WINDOW.getVirtualWidth() - self.BALL.getWidth()) // 2,
                         self.WINDOW.getVirtualHeight() - self.BALL.getHeight() - 30)
        self.PLAYER.setPOS(((self.WINDOW.getVirtualWidth() - self.PLAYER.getWidth()) // 2),
                           self.WINDOW.getVirtualHeight() - self.PLAYER.getHeight())

        self.LIVES.clear()
        for x in range(lives):
            heart = ImageSprite(Image.HEART)
            heart.setScale(8)
            heart.setPOS(2 + SPACING, 2)
            self.LIVES.append(heart)
            SPACING += heart.getWidth() + 2
        self.WINDOW.clearScreen()
        self.initiateLevel()

    def blit(self, OBJ):
        self.WINDOW.getScreen().blit(OBJ.getScreen(), OBJ.getPOS())

    def startTimer(self):
        self.COLLISION = True

    def updateTimer(self):
        if self.COLLISION:
            self.COLLISION_MS += self.COLLISION_TIMER.tick()
            if self.COLLISION_MS > 500:
                self.resetTimer()

    def resetTimer(self):
        self.COLLISION_MS = 0
        self.X_COLLISION = -5
        self.Y_COLLISION = -5
        self.COLLISION = False

    def updateBoard(self):
        self.PLAYERBOARD = pygame.draw.rect(self.WINDOW.getScreen(), pygame.Color(0, 0, 0, 128),
                                          pygame.Rect(self.PLAYER.getX()+2, self.PLAYER.getY(),
                                                      self.PLAYER.getWidth() - 4, 1))

    def updateCoins(self):
        self.COINS_TXT = Text(f"Coins: {self.SCORE}")
        self.COINS_TXT.setPOS(self.WINDOW.getVirtualWidth() - self.COINS_TXT.getWidth(), 0)

    def clearBrickTimer(self, BRICK=None):
        for brick in self.BRICKS:
            if brick != BRICK:
                brick.resetTime()

    def checkBrickCollision(self):
        POP = []
        X_COL = False
        Y_COL = False
        self.updateTimer()
        for x in range(len(self.BRICKS)):
            if self.getSpriteCollision(self.BRICKS[x], self.BALL):
                self.BRICKS[x].startTimer()
                COL = False
                self.startTimer()
                for X_WALLS in self.BRICKS[x].getXWalls():
                    if self.getSpriteCollision(X_WALLS, self.BALL):
                        if self.BRICKS[x].uptime() > 50:
                            COL = True
                        if X_WALLS.y != self.X_COLLISION:
                            self.BALL.invertDir(False, True)
                            self.X_COLLISION = X_WALLS.y
                            X_COL = True
                            self.clearBrickTimer(self.BRICKS[x])
                for Y_WALLS in self.BRICKS[x].getYWalls():
                    if self.getSpriteCollision(Y_WALLS, self.BALL):
                        if self.BRICKS[x].uptime() > 50:
                            COL = True
                            if Y_WALLS.x != self.Y_COLLISION:
                                self.Y_COLLISION = Y_WALLS.x
                                self.BALL.invertDir(True, False)
                                Y_COL = True
                                self.clearBrickTimer(self.BRICKS[x])
                if not (X_COL ^ Y_COL) and not (X_COL or Y_COL):
                    for CORNERS in self.BRICKS[x].getCorners():
                        if self.getSpriteCollision(CORNERS, self.BALL):
                            if self.BRICKS[x].uptime() > 50:
                                COL = True
                                self.BALL.invertDir(True, True)
                                self.clearBrickTimer(self.BRICKS[x])

                if COL:
                    IMAGE = self.BRICKS[x].getImage()
                    INDEX = Image.BRICKS.index(IMAGE)
                    if INDEX < 2:
                        self.BRICKS[x].setImage(Image.BRICKS[INDEX + 1])
                        self.WINDOW.getScreen().blit(self.BRICKS[x].getScreen(), self.BRICKS[x].getPOS())
                    else:
                        POP.append(x)
                        if randrange(5) == 2:
                            COIN = Coin(Image.COIN)
                            COIN.setScale(10)
                            COIN.setPOS(self.BRICKS[x].getX()+(self.BRICKS[x].getWidth() - COIN.getWidth())//2, self.BRICKS[x].getY()+(self.BRICKS[x].getHeight() - COIN.getHeight())//2)
                            self.COINS.append(COIN)
            else:
                self.WINDOW.getScreen().blit(self.BRICKS[x].getScreen(), self.BRICKS[x].getPOS())
        POP.sort(reverse=True)
        for x in POP:
            self.BRICKS.pop(x)

    def checkPlayerCollision(self):
        X_COL = False
        if self.getSpriteCollision(self.PLAYER, self.BALL):
            self.clearBrickTimer()
            if self.getSpriteCollision(self.PLAYER.getXWalls()[0], self.BALL):
                self.resetTimer()
                self.BALL.invertDir(False, True)
                X_COL = True
            if not X_COL:
                self.BALL.invertDir(True, True)
                self.resetTimer()
                for CORNERS in self.PLAYER.getCorners():
                    if self.getSpriteCollision(CORNERS, self.BALL):
                        self.BALL.invertDir(True, True)

    def setMid(self, OBJECT):
        OBJECT.setPOS((self.WINDOW.getVirtualWidth()-OBJECT.getWidth())//2, (self.WINDOW.getVirtualHeight()-OBJECT.getHeight())//2)

    def checkCoins(self):
        POP = []
        for x in range(len(self.COINS)):
            TIMEOUT = self.COINS[x].updateTimer()
            if pygame.mouse.get_pressed(3)[0] and self.COINS[x].getRect().collidepoint(
                    pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.SCORE += 1
                self.updateCoins()
                POP.insert(0, x)
            elif TIMEOUT:
                POP.insert(0, x)
        for x in POP:
            self.COINS.pop(x)

    def run(self):
        while True:
            # inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # Game Mechanics
            if self.STARTGAME:
                KEYPRESSES = pygame.key.get_pressed()
                self.WINDOW.clearScreen()
                self.PLAYER.updateWalls(self.WINDOW.getScreen(), 2)
                self.blit(self.PLAYER)
                self.checkCoins()
                for coin in self.COINS:
                    self.blit(coin)
                BUTTON = pygame.draw.rect(self.WINDOW.getScreen(), Color.WHITE, (self.WINDOW.getVirtualWidth()-5, self.WINDOW.getVirtualHeight()-5, 5, 5))
                if pygame.mouse.get_pressed(3)[0] and BUTTON.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    self.BALL.setSpeed(self.BALL.getSpeed()+5)
                self.updateCoins()
                self.blit(self.COINS_TXT)
                self.PLAYER.adMoveChkBoundaries(KEYPRESSES, self.WINDOW.getVirtualWidth())
                self.checkPlayerCollision()
                CHANGED = self.BALL.bounce(self.WINDOW)
                if CHANGED:
                    self.clearBrickTimer()
                if len(self.BRICKS) == 0:
                    self.GAME_OVER = True
                    self.STARTGAME = False
                    self.GAME_OVER_TXT.setText("Level Cleared!")
                    self.GAME_OVER_TXT.setColor(Color.GREEN)
                    self.setMid(self.GAME_OVER_TXT)
                else:
                    self.checkBrickCollision()
                if self.BALL.getY()+self.BALL.getHeight()-2> self.WINDOW.getVirtualHeight():
                    if len(self.LIVES) > 1:
                        self.LIVES.pop(len(self.LIVES)-1)
                        self.BALL.setPOS((self.WINDOW.getVirtualWidth()-self.BALL.getWidth())//2, 7*(self.WINDOW.getVirtualHeight()-self.BALL.getHeight())//8)
                        self.BALL.reset()
                        self.resetTimer()
                    else:
                        self.GAME_OVER_TXT.setText("Level Failed!")
                        self.GAME_OVER_TXT.setColor(Color.RED)
                        self.setMid(self.GAME_OVER_TXT)
                        self.GAME_OVER = True
                        self.STARTGAME = False
                self.blit(self.BALL)
                for heart in self.LIVES:
                    self.blit(heart)
                self.WINDOW.updateFrame()
            # Start Menu
            elif self.MENU:
                self.initiateStartMenu()
                if self.EASY_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVEREASY)
                    self.blit(x)
                    if pygame.mouse.get_pressed(3)[0]:
                        self.DIFFICULTY = 1
                        self.startGame(3)
                elif pygame.mouse.get_pressed(3)[0] and self.MED_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVERMED)
                    self.blit(x)
                    if pygame.mouse.get_pressed(3)[0]:
                        self.DIFFICULTY = 2
                        self.startGame(2)
                elif self.HARD_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVERHARD)
                    self.blit(x)
                    if pygame.mouse.get_pressed(3)[0]:
                        self.DIFFICULTY = 3
                        self.startGame(1)
                self.WINDOW.updateFrame()
            elif not self.STARTGAME and not self.GAME_OVER and not self.MENU:
                self.WINDOW.clearScreen()
                for brick in self.BRICKS:
                    self.blit(brick)
                self.blit(self.PLAYER)
                self.blit(self.BALL)
                TEXT = Text("Press the spacebar to start")
                self.setMid(TEXT)
                self.blit(TEXT)
                self.WINDOW.updateFrame()
                KEYPRESSES = pygame.key.get_pressed()
                if KEYPRESSES[pygame.K_SPACE] == 1:
                    self.STARTGAME = True
            elif self.GAME_OVER and not self.MENU and not self.STARTGAME:
                self.WINDOW.clearScreen()
                for brick in self.BRICKS:
                    self.blit(brick)
                self.blit(self.PLAYER)
                self.blit(self.BALL)
                self.blit(self.GAME_OVER_TXT)
                self.STARTGAME = False
                TEXT = Text("Press the spacebar to continue")
                TEXT.setFontSize(30)
                TEXT.setPOS((self.WINDOW.getVirtualWidth()-TEXT.getWidth())//2, (self.WINDOW.getVirtualHeight()-TEXT.getHeight())//2+self.GAME_OVER_TXT.getHeight()+5)
                self.blit(TEXT)
                self.WINDOW.updateFrame()
                KEYPRESSES = pygame.key.get_pressed()
                if KEYPRESSES[pygame.K_SPACE] == 1:
                    self.MENU = True
