"""
Title: Brick Breaker Game Engine
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame
from window import Window
from imageSprite import ImageSprite
from loader import Color, Image
from text import Text
from random import randrange

class Game:
    pygame.init()
    def __init__(self):
        ## Setup
        self.WINDOW = Window()
        self.WINDOW.setBackgroundImage(Image.BACKGROUND)
        self.TITLE = ImageSprite(Image.TITLE)
        self.TITLE.setPOS((self.WINDOW.getVirtualWidth()-self.TITLE.getWidth())//2, 50)
        """
        self.PLAYER = ImageSprite(Image.PLAYER)
        self.PLAYER.setScale(2)
        self.PLAYER.setPOS(((self.WINDOW.getVirtualWidth()-self.PLAYER.getWidth())//2), ((self.WINDOW.getVirtualHeight() - self.PLAYER.getHeight())//2))
"""
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
        self.LIVES = 3
        self.LIVES_TXT = Text(f"Lives Left: {self.LIVES}")

        # Bricks
        self.BRICKS = []
        for brick in Image.BRICKS:
            self.BRICKS.append(ImageSprite(brick).setScale(2))

        # Coins
        self.COINS = 0
        self.COINS_TXT = Text(f"Score: {self.COINS}")

        # Timer
        self.TIMER = pygame.time.Clock()
        self.TIMER_MS = 0
        self.TIME_LEFT = 15
        self.TIME_TXT = Text(f"Time Left: {self.TIME_LEFT}")
        self.TIME_TXT.setPOS(self.WINDOW.getVirtualWidth()-self.TIME_TXT.getWidth(), 0)

        # Game Over
        self.GAME_OVER_TXT = Text("Game Over!", COLOR=Color.RED)
        self.GAME_OVER = False
        self.GAME_OVER_TXT.setFontSize(50)
        self.GAME_OVER_TXT.setPOS((self.WINDOW.getVirtualWidth()-self.GAME_OVER_TXT.getWidth())//2, (self.WINDOW.getVirtualHeight()-self.GAME_OVER_TXT.getHeight())//2)

    def initiateStartMenu(self):
        self.WINDOW.clearScreen()
        self.WINDOW.getScreen().blit(self.TITLE.getScreen(), self.TITLE.getPOS())
        self.WINDOW.getScreen().blit(self.EASY_IMG.getScreen(), self.EASY_IMG.getPOS())
        self.WINDOW.getScreen().blit(self.MED_IMG.getScreen(), self.MED_IMG.getPOS())
        self.WINDOW.getScreen().blit(self.HARD_IMG.getScreen(), self.HARD_IMG.getPOS())
        self.WINDOW.updateFrame()

    def placeBricks(self, levels):
        # Place bricks on screen
        while True:
            self.WINDOW.getScreen().blit()

    def getSpriteCollision(self, SPRITE, SPRITE2):
        if pygame.Rect.colliderect(SPRITE.getRect(), SPRITE2.getRect()):
            return True
        else:
            return False

    def updateTimer(self):
        self.TIMER_MS += self.TIMER.tick()
        if self.TIMER_MS > 1000 and self.TIME_LEFT > 0:
            self.TIME_LEFT -= 1
            self.TIME_TXT.setText(f"Time Left: {self.TIME_LEFT}")
            self.TIMER_MS = 0

    def initiateLevel(self):
        self.WINDOW.clearScreen()
        self.WINDOW.setBackgroundImage(Image.BACKGROUND)
        if self.DIFFICULTY == 1:
            self.placeBricks(3)

    def run(self):
        while True:
            # inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.initiateStartMenu()
            if self.GAME_OVER:
                self.initiateStartMenu()
                if pygame.mouse.get_pressed(1)[0] and pygame.Rect.colliderect(self.EASY_IMG.RECT, pygame.mouse.get_pos()):
                    self.DIFFICULTY = 1
                    self.GAME_OVER = False
                elif pygame.mouse.get_pressed(1)[0] and pygame.Rect.colliderect(self.MED_IMG.RECT, pygame.mouse.get_pos()):
                    self.DIFFICULTY = 2
                    self.GAME_OVER = False
                elif pygame.mouse.get_pressed(1)[0] and pygame.Rect.colliderect(self.HARD_IMG.RECT, pygame.mouse.get_pos()):
                    self.DIFFICULTY = 3
                    self.GAME_OVER = False
            else:
                self.initiateLevel()

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