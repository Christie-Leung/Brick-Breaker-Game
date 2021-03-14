"""
Title: Coin class
Author: Christie Leung
Date Created: 2021-03-11
"""
import pygame

from imageSprite import ImageSprite


class Coin(ImageSprite):
    def __init__(self, IMAGE_FILE):
        super().__init__(IMAGE_FILE)
        self.TIMER = pygame.time.Clock()
        self.TIME_LEFT = 5
        self.TIME_MS = 0

    def updateTimer(self):
        # Timer for each coin to determine whether 5 seconds have passed
        self.TIME_MS += self.TIMER.tick()
        if self.TIME_MS > 1000 and self.TIME_LEFT != 0:
            self.TIME_MS = 0
            self.TIME_LEFT -= 1
            return False
        elif self.TIME_LEFT == 0:
            return True