"""
Title: Text Class
Author: Christie Leung
Date Created: 2021-03-08
"""

from loader import Color
import pygame
from sprites import Sprite

class Text(Sprite):
    def __init__(self, TEXT="Hello World", COLOR=Color.WHITE):
        super().__init__()
        self.TEXT = TEXT
        self.COLOR = COLOR
        self.FONT = pygame.font.SysFont("Lato", 36)
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

    def setText(self, text):
        self.TEXT = text
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

    def setFontSize(self, Size):
        self.FONT = pygame.font.SysFont("Lato", Size)
        self.SCREEN = self.FONT.render(self.TEXT, True, self.COLOR)

if __name__ == '__main__':
    from window import Window

    pygame.init()
    WINDOW = Window()
    TEXT = Text()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        WINDOW.getScreen().blit(TEXT.getScreen(), TEXT.getPOS())
        WINDOW.updateFrame()

