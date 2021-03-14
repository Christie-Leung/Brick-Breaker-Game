"""
Title: Brick Breaker Game Engine
Author: Christie Leung
Date Created: 2021-03-08
"""

from random import randrange

import pygame

from bricks import Brick
from coin import Coin
from imageSprite import ImageSprite
from loader import Color, Image
from shop import ShopItem
from text import Text
from window import Window


class Game:
    pygame.init()
    def __init__(self):
        ## Setup
        self.WINDOW = Window()
        self.WINDOW.setBackgroundImage(Image.BACKGROUND)
        self.TITLE = ImageSprite(Image.TITLE)
        self.TITLE.setPOS((self.WINDOW.getVirtualWidth()-self.TITLE.getWidth())//2, 50)

        self.STARTGAME = False
        self.MENU = True

        # Ball
        self.BALL = ImageSprite(Image.WRECKITRALPH)
        self.BALL.setScale(14)
        # Paddle
        self.PLAYER = Brick(Image.PLAYER)
        self.PLAYER.setScale(8)
        self.PLAYER.setSpeed(8)

        #Difficulty
        self.EASY_IMG = ImageSprite(Image.EASY)
        self.EASY_IMG.setScale(2.1)
        self.EASY_IMG.setPOS((self.WINDOW.getVirtualWidth() - self.EASY_IMG.getWidth()) // 2,
                             13 * (2 * self.WINDOW.getVirtualHeight() // 3 - self.EASY_IMG.getHeight()) // 16)
        self.MED_IMG = ImageSprite(Image.MED)
        self.MED_IMG.setScale(2.1)
        self.MED_IMG.setPOS((self.WINDOW.getVirtualWidth() - self.MED_IMG.getWidth()) // 2,
                            self.EASY_IMG.getY() + self.EASY_IMG.getHeight() + 5)
        self.HARD_IMG = ImageSprite(Image.HARD)
        self.HARD_IMG.setScale(2.1)
        self.HARD_IMG.setPOS((self.WINDOW.getVirtualWidth() - self.HARD_IMG.getWidth()) // 2,
                             self.MED_IMG.getY() + self.MED_IMG.getHeight() + 5)
        self.DIFFICULTY = 0

        # SHOP
        self.SHOP = ImageSprite(Image.SHOP)
        self.SHOP.setScale(2.1)
        self.SHOP.setPOS((self.WINDOW.getVirtualWidth() - self.SHOP.getWidth()) // 2,
                         self.HARD_IMG.getY() + self.HARD_IMG.getHeight() + 5)
        self.INSHOP = False
        self.CUSTOMIZATION = [ShopItem(Image.BACKGROUND, -1, True), ShopItem(Image.BACKGROUND1, 50),
                              ShopItem(Image.BACKGROUND2, 100), ShopItem(Image.WRECKITRALPH, -1, True),
                              ShopItem(Image.BALL1, 50), ShopItem(Image.BALL2, 100)]

        # Lives
        self.LIVES = []

        # Bricks
        self.TEMPLATE = ImageSprite(Image.BRICKS[0])
        self.TEMPLATE.setScale(5)
        self.BRICKS = []

        # Brick Collision
        self.TIME_LEFT = 3
        self.TIMER = pygame.time.Clock()
        self.MS = 0
        self.COLLISION = False
        self.X_COLLISION = -5
        self.Y_COLLISION = -5
        self.TIMER_ON = False

        # Coins
        self.COINS = []
        self.SCORE = 0
        self.COINS_TXT = Text(f"Coins: {self.SCORE}")

        # Game Over
        self.GAME_OVER_TXT = Text("Game Over!")
        self.GAME_OVER = False
        self.GAME_OVER_TXT.setFontSize(50)
        self.GAME_OVER_TXT.setPOS((self.WINDOW.getVirtualWidth()-self.GAME_OVER_TXT.getWidth())//2, (self.WINDOW.getVirtualHeight()-self.GAME_OVER_TXT.getHeight())//2)

    ## Initiations
    def initiateStartMenu(self):
        """
        Initiates Start Menu Screen
        """
        self.WINDOW.clearScreen()
        self.updateCoins()
        self.blit(self.TITLE)
        self.blit(self.EASY_IMG)
        self.blit(self.MED_IMG)
        self.blit(self.HARD_IMG)
        self.blit(self.SHOP)

    def initiateShop(self):
        """
        Initiates Shop Screen
        """
        self.WINDOW.clearScreen()

        # Places "Store" Text at the top of screen
        STORE_TEXT = Text("Store")
        STORE_TEXT.setPOS((self.WINDOW.getVirtualWidth() - STORE_TEXT.getWidth()) // 2, 10)
        self.blit(STORE_TEXT)

        # Displays all customizable items in a neat format
        X = 0
        Y = 0
        WIDTH = self.WINDOW.getVirtualWidth() // 3
        PADDING = STORE_TEXT.getY() + STORE_TEXT.getHeight()
        HEIGHT = (self.WINDOW.getVirtualHeight() - 4 * PADDING) // 2
        NEW_CUSTOMIZATION = []
        for item in self.CUSTOMIZATION:
            item.updateStatus()
            if Y == 0:
                item.fixedScale(WIDTH - 30, 120)
            else:
                item.fixedScale(WIDTH - 70, HEIGHT - 10)
            item.setPOS((WIDTH - item.getWidth()) // 2 + (X * WIDTH),
                        (HEIGHT - item.getHeight()) // 2 + (Y * HEIGHT) + 2 * PADDING)
            item.updatePOS()
            item.updatePricePos()
            self.blit(item.getPriceText())
            self.blit(item)
            NEW_CUSTOMIZATION.append(item)
            X += 1
            if X == 3:
                Y += 1
                X = 0
        self.blit(self.COINS_TXT)
        self.CUSTOMIZATION.clear()
        self.CUSTOMIZATION = NEW_CUSTOMIZATION

    def initiateBricks(self, levels):
        # Place bricks on screen
        self.BRICKS.clear()
        self.COINS.clear()
        X = 55
        X_PADDING = 20
        Y = 40
        for i in range(levels):
            WIDTHLEFT = self.WINDOW.getVirtualWidth() - (2 * X_PADDING)
            SPACE = 5
            BRICK_WIDTH = self.TEMPLATE.getWidth()
            if (i+1) % 2 == 0:
                WIDTHLEFT -= BRICK_WIDTH
            while WIDTHLEFT - BRICK_WIDTH > 0:
                WIDTHLEFT -= BRICK_WIDTH + SPACE
                BRICK = Brick(Image.BRICKS[0])
                BRICK.setScale(5)
                BRICK.setPOS(X, Y)
                X += BRICK_WIDTH + SPACE
                self.BRICKS.append(BRICK)
                BRICK.updateWalls(self.WINDOW.getScreen())
                self.blit(BRICK)
            if i % 2 == 0:
                X = 55 + BRICK_WIDTH//2
            else:
                X = 55
            Y += SPACE + self.TEMPLATE.getHeight()
        self.blit(self.BALL)
        self.blit(self.PLAYER)
        self.WINDOW.updateFrame()

    def initiateLevel(self):
        """
        Initiates bricks and ball speed for each difficulty level
        """
        if self.DIFFICULTY == 1:
            self.initiateBricks(3)
            self.BALL.setSpeed(4)
        if self.DIFFICULTY == 2:
            self.initiateBricks(4)
            self.BALL.setSpeed(6)
        if self.DIFFICULTY == 3:
            self.initiateBricks(5)
            self.BALL.setSpeed(8)

    def startGame(self, lives):
        """
        Starts a new game and clears previous data/reset positions
        :param lives: number of lives given
        """
        self.GAME_OVER = False
        self.MENU = False
        SPACING = 0
        self.BALL.setPOS((self.WINDOW.getVirtualWidth() - self.BALL.getWidth()) // 2,
                         self.WINDOW.getVirtualHeight() - self.BALL.getHeight() - 30)
        self.PLAYER.setPOS(((self.WINDOW.getVirtualWidth() - self.PLAYER.getWidth()) // 2),
                           self.WINDOW.getVirtualHeight() - self.PLAYER.getHeight())

        self.LIVES.clear()
        for x in range(lives):
            heart = ImageSprite(Image.HEART)
            heart.setScale(8)
            heart.setPOS(5 + SPACING, 5)
            self.LIVES.append(heart)
            SPACING += heart.getWidth() + 2
        self.WINDOW.clearScreen()
        self.initiateLevel()

    ## Collisions
    def getSpriteCollision(self, SPRITE, SPRITE2):
        """
        Detect if there is a collision between two sprites
        :param SPRITE: first sprite object
        :param SPRITE2: second sprite object
        :return: whether collision occurred
        """
        try:
            if pygame.Rect.colliderect(SPRITE.getRect(), SPRITE2.getRect()):
                return True
            else:
                return False
        except AttributeError:
            if pygame.Rect.colliderect(SPRITE, SPRITE2.getRect()):
                return True
            else:
                return False

    def checkBrickCollision(self):
        """
        Checks if the ball has hit a brick and determines the next course of action for the ball
        """
        POP = []
        X_COL = False
        Y_COL = False
        self.updateBrickTimer()
        for x in range(len(self.BRICKS)):
            if self.getSpriteCollision(self.BRICKS[x], self.BALL):
                self.BRICKS[x].startTimer()
                COL = False
                self.startBrickTimer()
                for X_WALLS in self.BRICKS[x].getXWalls():
                    if self.getSpriteCollision(X_WALLS, self.BALL):
                        if self.BRICKS[x].uptime() > 50:
                            COL = True
                        if X_WALLS.y != self.X_COLLISION:
                            self.BALL.invertDir(False, True)
                            self.X_COLLISION = X_WALLS.y
                            X_COL = True
                            self.clearBrickTimer(self.BRICKS[x])
                for Y_WALLS in self.BRICKS[x].getYWalls():
                    if self.getSpriteCollision(Y_WALLS, self.BALL):
                        if self.BRICKS[x].uptime() > 50:
                            COL = True
                            if Y_WALLS.x != self.Y_COLLISION:
                                self.Y_COLLISION = Y_WALLS.x
                                self.BALL.invertDir(True, False)
                                Y_COL = True
                                self.clearBrickTimer(self.BRICKS[x])
                if not (X_COL ^ Y_COL) and not (X_COL or Y_COL):
                    for CORNERS in self.BRICKS[x].getCorners():
                        if self.getSpriteCollision(CORNERS, self.BALL):
                            if self.BRICKS[x].uptime() > 50:
                                COL = True
                                self.BALL.invertDir(True, True)
                                self.clearBrickTimer(self.BRICKS[x])

                if COL:
                    IMAGE = self.BRICKS[x].getImage()
                    INDEX = Image.BRICKS.index(IMAGE)
                    if INDEX < self.DIFFICULTY - 1:
                        self.BRICKS[x].setImage(Image.BRICKS[INDEX + 1])
                        self.WINDOW.getScreen().blit(self.BRICKS[x].getScreen(), self.BRICKS[x].getPOS())
                    else:
                        POP.append(x)
                        if randrange(5) == 2:
                            COIN = Coin(Image.COIN)
                            COIN.setScale(10)
                            COIN.setPOS(self.BRICKS[x].getX() + (self.BRICKS[x].getWidth() - COIN.getWidth()) // 2,
                                        self.BRICKS[x].getY() + (self.BRICKS[x].getHeight() - COIN.getHeight()) // 2)
                            self.COINS.append(COIN)
            else:
                self.WINDOW.getScreen().blit(self.BRICKS[x].getScreen(), self.BRICKS[x].getPOS())
        POP.sort(reverse=True)
        for x in POP:
            self.BRICKS.pop(x)

    def checkPlayerCollision(self):
        # Checks if ball has collided with player
        X_COL = False
        if self.getSpriteCollision(self.PLAYER, self.BALL):
            self.clearBrickTimer()
            if self.getSpriteCollision(self.PLAYER.getXWalls()[0], self.BALL):
                self.resetTimer()
                self.BALL.invertDir(False, True)
                X_COL = True
            if not X_COL:
                self.BALL.invertDir(True, True)
                self.resetTimer()
                for CORNERS in self.PLAYER.getCorners():
                    if self.getSpriteCollision(CORNERS, self.BALL):
                        self.BALL.invertDir(True, True)

    ## Brick Timer
    def startBrickTimer(self):
        self.COLLISION = True

    def updateBrickTimer(self):
        """
        If Collision timer is on, the timer will be updated until reset
        :return:
        """
        if self.COLLISION:
            self.MS += self.TIMER.tick()
            if self.MS > 500:
                self.resetTimer()

    def resetTimer(self):
        """
        Resets brick timers
        """
        self.MS = 0
        self.X_COLLISION = -5
        self.Y_COLLISION = -5
        self.COLLISION = False

    def clearBrickTimer(self, BRICK=None):
        # Clears all brick timer except given Brick
        for brick in self.BRICKS:
            if brick != BRICK:
                brick.resetTime()

    ## Shop Timer
    def startShopTimer(self):
        self.TIMER_ON = True

    def updateShopTimer(self):
        """
        if shop timer is on, it will be updated until timer is off (used for displaying error message)
        """
        if self.TIMER_ON:
            self.MS += self.TIMER.tick()
            if self.MS > 1000 and self.TIME_LEFT != 0:
                self.TIME_LEFT -= 1
                self.MS = 0
            elif self.TIME_LEFT == 0:
                self.TIMER_ON = False
                self.TIME_LEFT = 3
                self.MS = 0

    ## Updates
    def updateBoard(self):
        """
        Updates wall in playerboard
        """
        self.PLAYERBOARD = pygame.draw.rect(self.WINDOW.getScreen(), pygame.Color(0, 0, 0, 128),
                                            pygame.Rect(self.PLAYER.getX() + 2, self.PLAYER.getY(),
                                                        self.PLAYER.getWidth() - 4, 1))

    def updateCoins(self):
        # Updates Coin text
        self.COINS_TXT = Text(f"Coins: {self.SCORE}")
        self.COINS_TXT.setPOS(self.WINDOW.getVirtualWidth() - self.COINS_TXT.getWidth() - 5, 5)

    def checkCoins(self):
        """
        Checks if a coin has been clicked or timed out
        """
        POP = []
        for x in range(len(self.COINS)):
            TIMEOUT = self.COINS[x].updateTimer()
            if pygame.mouse.get_pressed(3)[0] and self.COINS[x].getRect().collidepoint(
                    pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.SCORE += 1
                self.updateCoins()
                POP.insert(0, x)
            elif TIMEOUT:
                POP.insert(0, x)
        for x in POP:
            self.COINS.pop(x)

    ## Utilities
    def blit(self, OBJ):
        """
        Shortcut for displaying objects on a window
        :param OBJ: Object being displayed
        """
        self.WINDOW.getScreen().blit(OBJ.getScreen(), OBJ.getPOS())

    def setMid(self, OBJECT):
        # Sets an Object into the middle of the screen
        OBJECT.setPOS((self.WINDOW.getVirtualWidth() - OBJECT.getWidth()) // 2,
                      (self.WINDOW.getVirtualHeight() - OBJECT.getHeight()) // 2)

    def run(self):
        while True:
            # inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # Game Mechanics
            if self.STARTGAME:
                KEYPRESSES = pygame.key.get_pressed()
                self.WINDOW.clearScreen()

                ## Player
                self.PLAYER.updateWalls(self.WINDOW.getScreen(), 2)
                self.blit(self.PLAYER)
                self.PLAYER.adMoveChkBoundaries(KEYPRESSES, self.WINDOW.getVirtualWidth())
                self.checkPlayerCollision()

                ## Coins
                self.checkCoins()
                for coin in self.COINS:
                    self.blit(coin)
                self.updateCoins()
                self.blit(self.COINS_TXT)

                ## Ball Collisions
                CHANGED = self.BALL.bounce(self.WINDOW)
                if CHANGED:
                    self.clearBrickTimer()

                if len(self.BRICKS) == 0:  # Game Cleared
                    self.GAME_OVER = True
                    self.STARTGAME = False
                    self.SCORE += 10 * self.DIFFICULTY
                    self.updateCoins()
                    self.GAME_OVER_TXT.setText("Level Cleared!")
                    self.GAME_OVER_TXT.setColor(Color.GREEN)
                    self.setMid(self.GAME_OVER_TXT)
                else:
                    self.checkBrickCollision()

                # Ball goes out bounds
                if self.BALL.getY() + self.BALL.getHeight() - 2 > self.WINDOW.getVirtualHeight():
                    self.STARTGAME = False
                    if len(self.LIVES) > 1:
                        self.LIVES.pop(len(self.LIVES) - 1)
                        self.BALL.setPOS((self.WINDOW.getVirtualWidth() - self.BALL.getWidth()) // 2,
                                         7 * (self.WINDOW.getVirtualHeight() - self.BALL.getHeight()) // 8)
                        self.BALL.reset()
                        self.resetTimer()
                    else:
                        self.GAME_OVER_TXT.setText("Level Failed!")
                        self.GAME_OVER_TXT.setColor(Color.RED)
                        self.setMid(self.GAME_OVER_TXT)
                        self.GAME_OVER = True
                        self.STARTGAME = False
                self.blit(self.BALL)

                ## Lives
                for heart in self.LIVES:
                    self.blit(heart)
                self.WINDOW.updateFrame()
            # Start Menu
            elif self.MENU:
                self.initiateStartMenu()
                # Beginner Level
                if self.EASY_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVEREASY)
                    x.setScale(2.1)
                    self.WINDOW.getScreen().blit(x.getScreen(), self.EASY_IMG.getPOS())
                    if pygame.mouse.get_pressed(3)[0]:
                        self.DIFFICULTY = 1
                        self.startGame(3)
                # Intermediate Level
                elif self.MED_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVERMED)
                    x.setScale(2.1)
                    self.WINDOW.getScreen().blit(x.getScreen(), self.MED_IMG.getPOS())
                    if pygame.mouse.get_pressed(3)[0]:
                        self.DIFFICULTY = 2
                        self.startGame(4)
                # Hard Level
                elif self.HARD_IMG.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVERHARD)
                    x.setScale(2.1)
                    self.WINDOW.getScreen().blit(x.getScreen(), self.HARD_IMG.getPOS())
                    if pygame.mouse.get_pressed(3)[0]:
                        self.DIFFICULTY = 3
                        self.startGame(5)
                # Shop
                elif self.SHOP.getRect().collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    x = ImageSprite(Image.HOVERSHOP)
                    x.setScale(2.1)
                    self.WINDOW.getScreen().blit(x.getScreen(), self.SHOP.getPOS())
                    if pygame.mouse.get_pressed(3)[0]:
                        self.INSHOP = True
                        self.MENU = False
                self.WINDOW.updateFrame()
            # Before game has started, ensures player hit the space bar before starting
            elif not self.STARTGAME and not self.GAME_OVER and not self.MENU and not self.INSHOP:
                self.WINDOW.clearScreen()
                for brick in self.BRICKS:
                    self.blit(brick)
                self.blit(self.PLAYER)
                self.blit(self.BALL)
                TEXT = Text("Press the spacebar to start")
                self.setMid(TEXT)
                self.blit(TEXT)
                self.WINDOW.updateFrame()
                KEYPRESSES = pygame.key.get_pressed()
                if KEYPRESSES[pygame.K_SPACE] == 1:
                    self.STARTGAME = True
            # After game has ended, ensures player is ready to move on
            elif self.GAME_OVER and not self.MENU and not self.STARTGAME and not self.INSHOP:
                self.WINDOW.clearScreen()
                for brick in self.BRICKS:
                    self.blit(brick)
                self.blit(self.PLAYER)
                self.blit(self.BALL)
                self.blit(self.GAME_OVER_TXT)
                self.STARTGAME = False
                TEXT = Text("Press the spacebar to continue")
                TEXT.setFontSize(30)
                TEXT.setPOS((self.WINDOW.getVirtualWidth() - TEXT.getWidth()) // 2, (
                            self.WINDOW.getVirtualHeight() - TEXT.getHeight()) // 2 + self.GAME_OVER_TXT.getHeight() + 5)
                self.blit(TEXT)
                self.WINDOW.updateFrame()
                KEYPRESSES = pygame.key.get_pressed()
                if KEYPRESSES[pygame.K_SPACE] == 1:
                    self.MENU = True
            # Shop Menu
            elif self.INSHOP:
                self.initiateShop()
                self.updateShopTimer()
                DEACTIVATE = []
                CHANGED = 0

                # Back Button
                BACK = Text("<- Back")
                BACK.setColor(Color.GREEN)
                BACK.setPOS(10, 10)
                self.blit(BACK)
                if pygame.mouse.get_pressed(3)[0] and BACK.getRect().collidepoint(pygame.mouse.get_pos()[0],
                                                                                  pygame.mouse.get_pos()[1]):
                    self.INSHOP = False
                    self.MENU = True

                # Purchasing / Switching Customizations
                for x in range(len(self.CUSTOMIZATION)):
                    self.blit(self.CUSTOMIZATION[x])
                    if self.CUSTOMIZATION[x].getStatus():
                        DEACTIVATE.append(x)
                    if pygame.mouse.get_pressed(5)[0]:
                        if self.CUSTOMIZATION[x].getRect().collidepoint(pygame.mouse.get_pos()[0],
                                                                        pygame.mouse.get_pos()[1]):
                            if not self.CUSTOMIZATION[x].getStatus():
                                if self.CUSTOMIZATION[x].getPrice() == -1:
                                    self.CUSTOMIZATION[x].activate()
                                    CHANGED = x // 3 + 1
                                if self.SCORE >= self.CUSTOMIZATION[x].getPrice() and self.CUSTOMIZATION[
                                    x].getPrice() != -1:
                                    self.SCORE -= self.CUSTOMIZATION[x].getPrice()
                                    self.updateCoins()
                                    self.CUSTOMIZATION[x].purchase()
                                    if x < 3:
                                        self.WINDOW.setBackgroundImage(self.CUSTOMIZATION[x].getImage())
                                    else:
                                        self.BALL.setImage(self.CUSTOMIZATION[x].getImage())
                                    CHANGED = x // 3 + 1
                                elif self.SCORE < self.CUSTOMIZATION[x].getPrice():
                                    self.startShopTimer()
                            else:
                                if x < 3:
                                    self.WINDOW.setBackgroundImage(self.CUSTOMIZATION[x].getImage())
                                else:
                                    self.BALL.setImage(self.CUSTOMIZATION[x].getImage())

                # Change status of items if an item has been clicked
                if CHANGED > 0:
                    for x in DEACTIVATE:
                        if x // 3 + 1 == CHANGED:
                            self.CUSTOMIZATION[x].deactivate()

                # Error Message if user doesn't have enough coins
                if self.TIMER_ON:
                    ERROR = Text("You do not have enough coins!")
                    ERROR.setColor(Color.RED)
                    self.setMid(ERROR)
                    self.blit(ERROR)
                self.WINDOW.updateFrame()
