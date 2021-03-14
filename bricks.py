"""
Title: Brick Class
Author: Christie Leung
Date Created: 03-09-2021
"""

import pygame

from imageSprite import ImageSprite


# Inheritance of ImageSprite Class
class Brick(ImageSprite):
    def __init__(self, IMAGE_FILE):
        super().__init__(IMAGE_FILE)
        self.COLLISION_TIMER_MS = 0
        self.COLLISION_TIME_LEFT = 100
        self.TIMER = pygame.time.Clock()
        self.STARTTIMER = False
        self.X_WALLS = []
        self.Y_WALLS = []
        self.CORNERS = []

    # Modifier
    def startTimer(self):
        self.STARTTIMER = True

    def updateTimer(self):
        """
        Timer for each brick
        """
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

    def updateWalls(self, SCREEN, SIZE=5):
        """
        Updates imaginary blocks used to determine ball direction when collision occurs
        :param SCREEN: window screen
        :param SIZE: thickness of each wall
        """
        self.X_WALLS = [pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 200),
                                         pygame.Rect(self.X + SIZE, self.Y, self.getWidth() - 2 * SIZE, SIZE)),
                        pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 200),
                                         pygame.Rect(self.X + SIZE, self.Y + self.getHeight() - SIZE,
                                                     self.getWidth() - 2 * SIZE, SIZE))]
        self.Y_WALLS = [pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 200),
                                         pygame.Rect(self.X, self.Y + SIZE, SIZE, self.getHeight() - 2 * SIZE)),
                        pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 200),
                                         pygame.Rect(self.X + self.getWidth() - SIZE, self.Y + SIZE, SIZE,
                                                     self.getHeight() - 2 * SIZE))]
        self.CORNERS = [pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 200),
                                         pygame.Rect(self.X, self.Y, SIZE, SIZE)),
                        pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 128),
                                         pygame.Rect(self.X + self.getWidth() - SIZE, self.Y, SIZE, SIZE)),
                        pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 128),
                                         pygame.Rect(self.X, self.Y + self.getHeight() - SIZE, SIZE, SIZE)),
                        pygame.draw.rect(SCREEN, pygame.Color(255, 255, 255, 128),
                                         pygame.Rect(self.X + self.getWidth() - SIZE, self.Y + self.getHeight() - SIZE,
                                                     SIZE, SIZE))]

        # Accessor

    # Accessor
    def uptime(self):
        self.updateTimer()
        return self.COLLISION_TIME_LEFT

    def getXWalls(self):
        return self.X_WALLS

    def getYWalls(self):
        return self.Y_WALLS

    def getCorners(self):
        return self.CORNERS
