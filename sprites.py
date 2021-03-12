"""
Title: Sprite Class
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame


class Sprite:
    def __init__(self):
        self.WIDTH = 0
        self.HEIGHT = 0
        self.DIMENSION = (self.WIDTH, self.HEIGHT)
        self.SCREEN = None
        self.X = 0
        self.Y = 0
        self.POS = (self.X, self.Y)
        self.SPEED = 4
        self.RECT = None
        self.DIR_X = 1
        self.DIR_Y = -1

    # Modifier
    def setSpeed(self, speed):
        self.SPEED = speed

    def setPOS(self, X, Y):
        self.X = X
        self.Y = Y
        self.POS = (self.X, self.Y)

    def updatePOS(self):
        self.POS = (self.X, self.Y)

    def updateDimension(self):
        self.DIMENSION = (self.WIDTH, self.HEIGHT)

    def reset(self):
        self.DIR_X = 1
        self.DIR_Y = -1

    def invertDir(self, X, Y):
        if X:
            self.DIR_X = -self.DIR_X
        if Y:
            self.DIR_Y = -self.DIR_Y

    ## Movement
    def adMove(self, KEYPRESSES):
        if KEYPRESSES[pygame.K_d] == 1:
            self.X += self.SPEED
        if KEYPRESSES[pygame.K_a] == 1:
            self.X -= self.SPEED
        self.POS = (self.X, self.Y)

    def checkBoundaries(self, MAX_WIDTH, MIN_WIDTH=0):
        if self.X > MAX_WIDTH - self.getWidth():
            self.X = MAX_WIDTH - self.getWidth()
        elif self.X < MIN_WIDTH:
            self.X = MIN_WIDTH
        self.updatePOS()

    def adMoveChkBoundaries(self, KEYPRESSES, MAX_WIDTH,MIN_WIDTH=0):
        self.adMove(KEYPRESSES)
        self.checkBoundaries(MAX_WIDTH, MIN_WIDTH)

    def bounce(self, SCREEN):
        self.X = self.X + self.DIR_X * self.SPEED
        self.Y = self.Y + self.DIR_Y * self.SPEED
        CHANGED = False
        if self.X > SCREEN.getVirtualWidth() - self.getWidth():
            self.DIR_X = -1
            CHANGED = True
        if self.X < 0:
            self.DIR_X = 1
            CHANGED = True
        if self.Y < 0:
            self.DIR_Y = 1
            CHANGED = True

        """if self.Y > SCREEN.getVirtualHeight() - self.getHeight():
            self.DIR_Y = -1
            CHANGED = True"""
        self.POS = (self.X, self.Y)
        return CHANGED

    # Accessor
    def getScreen(self):
        return self.SCREEN

    def getPOS(self):
        return self.POS

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getWidth(self):
        return self.SCREEN.get_rect().width

    def getHeight(self):
        return self.SCREEN.get_rect().height

    def getRect(self):
        self.RECT = self.SCREEN.get_rect()
        self.RECT.x = self.X
        self.RECT.y = self.Y
        return self.RECT

    def getSpeed(self):
        return self.SPEED
