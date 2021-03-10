"""
Title: Brick Breaker Game Engine
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame
from window import Window
from sprites import Sprite
from imageSprite import ImageSprite
from loader import Color, Image
from text import Text
from bricks import Brick
from random import randrange

class Game:
    pygame.init()
    def __init__(self):
        ## Setup
        self.WINDOW = Window()
        self.WINDOW.setBackgroundImage(Image.BACKGROUND)
        self.TITLE = ImageSprite(Image.TITLE)
        self.TITLE.setPOS((self.WINDOW.getVirtualWidth()-self.TITLE.getWidth())//2, 50)
        self.BALL = ImageSprite(Image.WRECKITRALPH)
        self.BALL.setScale(14)
        self.BALL.setPOS((self.WINDOW.getVirtualWidth()-self.BALL.getWidth())//2, 7*(self.WINDOW.getVirtualHeight()-self.BALL.getHeight())//8)

        self.PLAYER = ImageSprite(Image.PLAYER)
        self.PLAYER.setScale(8)
        self.PLAYER.setSpeed(5)
        self.PLAYER.setPOS(((self.WINDOW.getVirtualWidth()-self.PLAYER.getWidth())//2), self.WINDOW.getVirtualHeight()-self.PLAYER.getHeight())

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

        # Coins
        self.COINS = 0
        self.COINS_TXT = Text(f"Score: {self.COINS}")

        # Game Over
        self.GAME_OVER_TXT = Text("Game Over!", COLOR=Color.RED)
        self.GAME_OVER = True
        self.GAME_OVER_TXT.setFontSize(50)
        self.GAME_OVER_TXT.setPOS((self.WINDOW.getVirtualWidth()-self.GAME_OVER_TXT.getWidth())//2, (self.WINDOW.getVirtualHeight()-self.GAME_OVER_TXT.getHeight())//2)

    def initiateStartMenu(self):
        self.WINDOW.clearScreen()
        self.WINDOW.getScreen().blit(self.TITLE.getScreen(), self.TITLE.getPOS())
        self.WINDOW.getScreen().blit(self.EASY_IMG.getScreen(), self.EASY_IMG.getPOS())
        self.WINDOW.getScreen().blit(self.MED_IMG.getScreen(), self.MED_IMG.getPOS())
        self.WINDOW.getScreen().blit(self.HARD_IMG.getScreen(), self.HARD_IMG.getPOS())
        self.WINDOW.updateFrame()

    def initiateBricks(self, levels):
        # Place bricks on screen
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
            if i % 2 == 0:
                X = 55 + BRICK_WIDTH//2
            else:
                X = 55
            Y += SPACE + self.TEMPLATE.getHeight()


    def getSpriteCollision(self, SPRITE, SPRITE2):
        if pygame.Rect.colliderect(SPRITE.getRect(), SPRITE2.getRect()):
            return True
        else:
            return False

    def initiateLevel(self):
        if self.DIFFICULTY == 1:
            self.initiateBricks(5)

    def startGame(self, lives):
        self.GAME_OVER = False
        SPACING = 0
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

    def checkCollision(self):
        POP = []
        for x in range(len(self.BRICKS)):
            self.BRICKS[x].updateTimer()
            if self.getSpriteCollision(self.BRICKS[x], self.BALL) and self.BRICKS[x].uptime() == 100:
                self.BRICKS[x].startTimer()
                self.BALL.invertDir()
                IMAGE = self.BRICKS[x].getImage()
                INDEX = Image.BRICKS.index(IMAGE)
                if INDEX < 2:
                    self.BRICKS[x].setImage(Image.BRICKS[INDEX + 1])
                    self.WINDOW.getScreen().blit(self.BRICKS[x].getScreen(), self.BRICKS[x].getPOS())
                else:
                    POP.insert(0, x)
                    self.BALL.invertDir()
                break
            else:
                self.WINDOW.getScreen().blit(self.BRICKS[x].getScreen(), self.BRICKS[x].getPOS())
        for x in POP:
            self.BRICKS.pop(x)

    def run(self):
        while True:
            # inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # Start Menu
            if self.GAME_OVER:
                self.initiateStartMenu()
                if pygame.mouse.get_pressed(3)[0] and self.EASY_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    self.DIFFICULTY = 1
                    self.startGame(3)
                elif pygame.mouse.get_pressed(3)[0] and pygame.Rect.collidepoint(self.MED_IMG.RECT, pygame.mouse.get_pos()):
                    self.DIFFICULTY = 2
                    self.startGame(2)
                elif pygame.mouse.get_pressed(3)[0] and pygame.Rect.collidepoint(self.HARD_IMG.RECT, pygame.mouse.get_pos()):
                    self.DIFFICULTY = 3
                    self.startGame(1)
            else:
                # Game Mechanics
                KEYPRESSES = pygame.key.get_pressed()
                self.WINDOW.clearScreen()
                self.blit(self.PLAYER)
                self.PLAYER.adMoveChkBoundaries(KEYPRESSES, self.WINDOW.getVirtualWidth())
                if pygame.Rect.colliderect(self.PLAYER.getRect(), self.BALL.getRect()):
                    self.BALL.invertDir()
                self.BALL.bounce(self.WINDOW)
                for brick in self.BRICKS:
                    self.blit(brick)
                    self.checkCollision()
                if self.BALL.getY() > self.WINDOW.getVirtualHeight():
                    if len(self.LIVES) > 1:
                        self.LIVES.pop(len(self.LIVES)-1)
                        self.BALL.setPOS((self.WINDOW.getVirtualWidth()-self.BALL.getWidth())//2, 7*(self.WINDOW.getVirtualHeight()-self.BALL.getHeight())//8)
                        self.BALL.reset()
                    else:
                        self.GAME_OVER = True
                        self.blit(self.GAME_OVER_TXT)
                        self.WINDOW.updateFrame()
                self.blit(self.BALL)
                for heart in self.LIVES:
                    self.blit(heart)
                self.WINDOW.updateFrame()

            """
            if not self.GAME_OVER:
                KEYS_PRESSED = pygame.key.get_pressed()
                # processing
                self.PLAYER.wasdMoveChkBoundaries(KEYS_PRESSED, self.WINDOW.getVirtualWidth(), self.WINDOW.getVirtualHeight())

                self.updateTimer()
                if self.TIME_LEFT == 0:
                    self.GAME_OVER = True

                # outputs
                self.WINDOW.clearScreen()
                self.WINDOW.getScreen().blit(self.PLAYER.getScreen(), self.PLAYER.getPOS())


                self.WINDOW.getScreen().blit(self.COINS_TXT.getScreen(), self.COINS_TXT.getPOS())
                self.WINDOW.getScreen().blit(self.TIME_TXT.getScreen(), self.TIME_TXT.getPOS())
                self.WINDOW.updateFrame()
            else:
                self.WINDOW.getScreen().blit(self.GAME_OVER_TXT.getScreen(), self.GAME_OVER_TXT.getPOS())
                self.WINDOW.updateFrame()
"""