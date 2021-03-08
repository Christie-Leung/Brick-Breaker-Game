# CSE3130 Project - Brick Breaker

This program is made in Python 3.8 and requires pygame to be installed. Assets folder included in this repository holds all images used in game.

## Game Description & Objective
The user is first prompted with a start menu, allowing them to choose their desired difficulty level. Once the difficulty level has been chosen, the game will be initiated with bricks at the top, and a ball at the bottom. 

__Objective__: Control the bar at the bottom by _moving your cursor_ to allow the ball to bounce back up, hitting all the bricks to successfully win the game.

Some bricks will drop coins in which the player would need to __use the mouse to click on it__ in order to collect it. Once the coin's timer runs out, it will disappear, and the player will lose the opportunity to collect them. 

(These coins allow players to change the layout of the game, including background image and ball colours.) *do this if enough time*

## Project Flowchart & UML Table

[Flowchart](ProjectFlowchart.png)
[UMLTable](ProjectUml.png)

### Encapsulation

### Polymorphism

### Inheritance
As seen in the UML Table above, the Text and ImageSprite classes inherit the attributes and methods of the Sprite class. It allows these classes to hold the same attributes and methods while also having additional variables.

### Aggregation
As described in the section above, as methods are in both classes that inherit the Sprite class, they can use those same functions, obtaining different results from each method according to the called object.