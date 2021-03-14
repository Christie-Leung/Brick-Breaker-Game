# CSE3130 Project - Brick Breaker

This program is made in Python 3.8 and requires pygame to be installed. Assets folder included in this repository holds
all images used in game.

## Game Description & Objective

The user is first prompted with a start menu, allowing them to choose their desired difficulty level. Once the
difficulty level has been chosen, the game will be initiated with bricks at the top, and a ball at the bottom.

[Start Menu](assets/startMenu.png)

__Objective__: Control the bar at the bottom by _using your a and d or left and right key_ to allow the ball to bounce
back up, hitting all the bricks to successfully win the game.

[Game](assets/game.png)

Some bricks will drop coins in which the player would need to __use the mouse to click on it__ in order to collect it.
Once the coin's timer runs out, it will disappear, and the player will lose the opportunity to collect them.

These coins allow players to customize the layout of the game.

[Store Menu](assets/storeMenu.png)

## Project Flowchart & UML Table

[Flowchart](ProjectFlowchart.png)
[UMLTable](ProjectUml.png)

### Encapsulation

Each Table in the UML Table depicts a class that holds variables and methods.

### Inheritance

As seen in the UML Table above, the Text and ImageSprite classes inherit the attributes and methods of the Sprite class.
It allows these classes to hold the same attributes and methods while also having additional variables.

### Aggregation

As described in the section above, as methods are in both classes that inherit the Sprite class, they can use those same
functions, obtaining different results from each method according to the called object.

### Polymorphism

Since some classes are aggregated, when the general methods of the parent class is called, they will give different
results, such as different images, widths or heights.

## Photo Credits:

Backgrounds:
https://pm1.narvii.com/6904/1ef7b698643b1eaf072414fa53df8977dda263e0r1-1919-1081v2_hq.jpg
https://wallpaperaccess.com/full/3003352.jpg
https://c4.wallpaperflare.com/wallpaper/765/580/971/digital-art-pixel-art-pixels-landscape-wallpaper-preview.jpg

Ball:
https://i.pinimg.com/originals/43/3e/9f/433e9f7787d8b9a303ea37680d7e453d.png
https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/ea231e53-e17c-4265-83b5-552457fc0505/d8uejr1-6fa24e3b-d69b-4764-b47a-5a19d1ca1970.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZWEyMzFlNTMtZTE3Yy00MjY1LTgzYjUtNTUyNDU3ZmMwNTA1XC9kOHVlanIxLTZmYTI0ZTNiLWQ2OWItNDc2NC1iNDdhLTVhMTlkMWNhMTk3MC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.4LuTgLlmBVvRCcm0EFDZzDN919OPlwYul37ab6S3euo
https://lh3.googleusercontent.com/proxy/isSuxCQ32aRPanDijcaGGKbT2qmuwtHorzBUjZOuf2YOQXvrmRDkgd1QcSkNauXGZM2UdNbTiH0vNPzOxC5vY6ssykYMM10h

Bricks: https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/676c614f-d09c-4485-a246-d1ea708273bd/dclu1p7-0e88ac70-c625-41ba-82bc-5ef23ec1bd7f.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvNjc2YzYxNGYtZDA5Yy00NDg1LWEyNDYtZDFlYTcwODI3M2JkXC9kY2x1MXA3LTBlODhhYzcwLWM2MjUtNDFiYS04MmJjLTVlZjIzZWMxYmQ3Zi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.qebEMer6_2U7OvDx2berz1eByKZRKptUHktiDVumeUs

Heart: https://opengameart.org/sites/default/files/heart%20pixel%20art%20254x254.png

Coin: https://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Coin-icon.png