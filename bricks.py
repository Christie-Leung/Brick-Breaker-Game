"""
Title: Brick Class
Author: Christie Leung
Date Created: 03-09-2021
"""

from imageSprite import ImageSprite
import pygame

class Brick(ImageSprite):
    def __init__(self, IMAGE_FILE):
        super().__init__(IMAGE_FILE)
        self.COLLISION_TIMER_MS = 0
        self.COLLISION_TIME_LEFT = 100
        self.TIMER = pygame.time.Clock()
        self.STARTTIMER = False

    # Modifier
    def startTimer(self):
        self.STARTTIMER = True

    def updateTimer(self):
        if self.STARTTIMER:
            self.COLLISION_TIMER_MS += self.TIMER.tick()
            if self.COLLISION_TIMER_MS > 1000 and self.COLLISION_TIME_LEFT > 0:
                self.COLLISION_TIME_LEFT -= 1
                self.TIMER_MS = 0
            if self.COLLISION_TIME_LEFT == 0:
                self.resetTime()

    def resetTime(self):
        self.COLLISION_TIME_LEFT = 100
        self.COLLISION_TIMER_MS = 0
        self.STARTTIMER = False

    # Accessor
    def uptime(self):
        return self.COLLISION_TIME_LEFT