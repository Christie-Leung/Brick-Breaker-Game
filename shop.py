"""
Title: Shop Class
Author: Christie Leung
Date Created: 20211-03-13
"""
from imageSprite import ImageSprite
from text import Text

# Inheritance of ImageSprite Class
class ShopItem(ImageSprite):
    def __init__(self, IMAGE_FILE, PRICE, ACTIVE=False):
        super().__init__(IMAGE_FILE)
        self.PRICE = PRICE
        self.PRICE_TXT = Text(f"Price: ${self.PRICE}")
        self.PRICE_TXT.setFontSize(20)
        self.ACTIVE = ACTIVE

    # Modifier
    def updateStatus(self):
        """
        Updates Price Text depending on status
        """
        if self.ACTIVE:
            self.PRICE_TXT.setText("Enabled")
        elif self.PRICE == -1 and not self.ACTIVE:
            self.PRICE_TXT.setText("Disabled")

    def fixedScale(self, WIDTH, HEIGHT):
        """
        Scales an item to fit a certain size
        :param WIDTH: Width of "box"
        :param HEIGHT: Height of "box"
        """
        if WIDTH < self.getWidth():
            SCALE_X = self.getWidth() / WIDTH
            self.setScale(SCALE_X)
        if HEIGHT < self.getHeight():
            SCALE_Y = self.getHeight() / HEIGHT
            self.setScale(1, SCALE_Y)

    def updatePricePos(self):
        self.PRICE_TXT.setPOS(self.getX() + (self.getWidth() + self.PRICE_TXT.getWidth()) // 2,
                              self.getY() + self.getHeight() + 5)

    def purchase(self):
        self.PRICE = -1
        self.ACTIVE = True

    def deactivate(self):
        self.ACTIVE = False

    def activate(self):
        self.ACTIVE = True

    # Accessor
    def getPriceText(self):
        return self.PRICE_TXT

    def getPrice(self):
        return self.PRICE

    def getStatus(self):
        return self.ACTIVE
