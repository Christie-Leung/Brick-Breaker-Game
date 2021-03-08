"""
Title: Image Sprites
Author: Christie Leung
Date Created: 2021-03-08
"""

from sprites import Sprite
import pygame

class ImageSprite(Sprite):
    def __init__(self, IMAGE_FILE):
        super().__init__()
        self.FILE_LOCATION = IMAGE_FILE
        self.SCREEN = pygame.image.load(self.FILE_LOCATION).convert_alpha()
        self.X_FLIP = False

    # Modifier
    def setScale(self, SCALE_X, SCALE_Y=0):
        if SCALE_Y == 0:
            SCALE_Y = SCALE_X
        self.SCREEN = pygame.transform.scale(self.SCREEN, (int(self.getWidth()//SCALE_X), int(self.getHeight()//SCALE_Y)))

