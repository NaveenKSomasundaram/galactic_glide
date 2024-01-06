# Galactic Glide: Laser Squadron
#### Description:
Blast through the cosmos in "Galactic Glide: Laser Squadron"! Navigate with your mouse, dodging asteroids with finesse. 
Unleash laser mayhem at the click of left mouse button, obliterating obstacles in your path. 
It's a stellar dance of precision and power—how far can your skills take you in this intergalactic escapade? 🖱️🚀

#### Video Demo: 
https://www.youtube.com/watch?v=etDluLRbbzQ

#### Version:
Test

#### About the game
This repository is made as a part of CS50's Introdction to Programming with python. 
It contains a simple retro style game developed in python. The intent is to have a simple and short game.
Moreover, a code artchitecture that allows to easily modify, add new elements and levels.

##### Gameplay

The mission is simple - avoid galactic obstacles and reach your destionation.

###### Laser Squadron
![alt text](/images/spaceship_01.png)

The Laser Squadron is a powerful voyager equipped with laser shots. Beware that you cannot have more than two active lasers at any instance.
###### Galactic Obstacles
![alt text](/images/asteroids/asteroid_01.png)
![alt text](/images/asteroids/asteroid_02.png)
![alt text](/images/asteroids/asteroid_03.png)


##### Control
 Move 🖱️ Left / Right to Glide and shoot laser by clicking left button.

### Development Details
The game is developed using pygame module.

#### Code Architecture
The key idea 💡 is to write some SOLID classes that can hopefully allow for a easily modifiable and extendable game.

#### Script
The current complexity allows for the game to coded in a single script, `./spacegame.py`. 
The classes representing various game entitities and helper functions are bundled in this script.

##### Game Resources
Sprites for the game such as spaceships, laser shots and asteroids are placed under `./images`.
Specifically, all obstacle sprites are placed under `./images/asteroids`.

##### Classes
A big dilemma is how to organize the classes. Keeping in mind potenitial expansions. The following classes are made
- `SpaceShip` Represents the spaceship 
- `LaserShots` Contains the active laser shots
- `Asteroids` Contains the active obstacles
- `ScrollingBackground` Used for the moving galactic background

Essentially, the classes should alllow to easily swap out sprites and modify behaviour. 
`LaserShots` object is used as an instance variable of `SpaceShip`. Composition seems to be appropriate here.
As the game complexity increases, inheritence must be connsidered. Moreover the classes must be moved to individual scripts.

### Future Development

###### Making the graphics seamless
The scrolling background behaviour can be enhanced. The current approach of looping the image does not work seamlessly.

###### Laser Shots- Obstacle interaction
The interaction approach has to be generalized. Also allow for shots that vanish after hitting an obstacle. 
Note that the current shot wipes out "all" obstacles on its way. 

###### Collision, Shooting Graphics
Gameplay can be improved by including graphics for collision, obliterating obstacles etc.

###### Sound effects




