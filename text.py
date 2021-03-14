"""
Title: Text Class
Author: Christie Leung
Date Created: 2021-03-08
"""

import pygame

from loader import Color
from sprites import Sprite


class Text(Sprite):
    def __init__(self, TEXT="Hello World", COLOR=Color.WHITE):
        super().__init__()
        self.TEXT = TEXT
        self.COLOR = COLOR
        self.FONT = pygame.font.SysFont("Lato", 36)
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

    # Modifier
    def setColor(self, Color):
        self.COLOR = Color
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

    def setText(self, text):
        self.TEXT = text
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

    def setFontSize(self, Size):
        self.FONT = pygame.font.SysFont("Lato", Size)
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

