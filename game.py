"""
Title: Brick Breaker Game Engine
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame
from window import Window
from imageSprite import ImageSprite
from loader import Color
from text import Text

class Game:
    pygame.init()
    def __init__(self):
        ## Setup
        self.WINDOW = Window()
        self.WINDOW.setBackgroundImage(Image.BACKGROUND)
        self.PLAYER = ImageSprite(Image.PLAYER)
        self.PLAYER.setScale(2)
        self.PLAYER.setPOS(((self.WINDOW.getVirtualWidth()-self.PLAYER.getWidth())//2), ((self.WINDOW.getVirtualHeight() - self.PLAYER.getHeight())//2))
        self.DIFFICULTY = 0

        # Lives
        self.LIVES = 3
        self.LIVES_TXT = Text(f"Lives Left: {self.LIVES}")

        # Bricks
        self.BRICKS =
        self.placeBricks()

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
        self.GAME_OVER_TXT.setPOS((self.WINDOW.getVirtualWidth()-self.GAME_OVER_TXT.getWidth())//2, (self.WINDOW.getVirtualHeight()-self.GAME_OVER_TEXT.getHeight())//2)

    def placeBricks(self):
        # Place bricks on screen

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

    def run(self):
        while True:
            # inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
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
