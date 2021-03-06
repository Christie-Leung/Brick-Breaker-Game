"""
Title: Windows
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame

from imageSprite import ImageSprite
from loader import Color


class Window:
    def __init__(self, TITLE="Brick Breaker", WIDTH=640, HEIGHT=480, FPS=60):
        self.TITLE = TITLE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.FPS = FPS
        self.SCREEN_DIMENSIONS = (self.WIDTH, self.HEIGHT)
        self.FRAME = pygame.time.Clock()
        self.SCREEN = pygame.display.set_mode(self.SCREEN_DIMENSIONS, pygame.SRCALPHA, 32)
        self.BACKGROUND = Color.GREY
        self.BACKGROUND_IMAGE = None
        self.SCREEN.fill(self.BACKGROUND)
        pygame.display.set_caption(self.TITLE)

    # Modifier
    def updateFrame(self):
        self.FRAME.tick(self.FPS)
        pygame.display.flip()

    def clearScreen(self):
        if self.BACKGROUND_IMAGE is None:
            self.SCREEN.fill(self.BACKGROUND)
        else:
            self.SCREEN.blit(self.BACKGROUND_IMAGE.getScreen(), self.BACKGROUND_IMAGE.getPOS())
            s = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((0, 0, 0, 128))  # notice the alpha value in the color
            self.SCREEN.blit(s, (0, 0))

    def setBackgroundColor(self, COLOR):
        self.BACKGROUND = COLOR
        self.clearScreen()

    def setBackgroundImage(self, IMAGE_FILE):
        self.BACKGROUND_IMAGE = ImageSprite(IMAGE_FILE)
        if self.BACKGROUND_IMAGE.getWidth() < self.getVirtualWidth():
            self.BACKGROUND_IMAGE.setScale(self.BACKGROUND_IMAGE.getWidth()/self.getVirtualWidth())
        if self.BACKGROUND_IMAGE.getHeight() < self.getVirtualHeight():
            self.BACKGROUND_IMAGE.setScale(self.BACKGROUND_IMAGE.getHeight()/self.getVirtualHeight())
        self.clearScreen()

    # Accessor
    def getScreen(self):
        return self.SCREEN

    def getVirtualWidth(self):
        return self.SCREEN.get_rect().width

    def getVirtualHeight(self):
        return self.SCREEN.get_rect().height
