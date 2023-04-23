# Fruit-Basket-hoop-shooter-game
1st year academic project in python with the library pygame

![image](https://user-images.githubusercontent.com/123560349/233855724-b784b51a-9a7e-465b-8e79-b9142bbbf199.png)

## Game Explanation
The aim of the game is simple: score as many points as possible by throwing fruits through a basketball hoop. The trajectory of the projectiles is calculated using second degree equations from solid dynamics. Each fruit has different properties, such as mass and size, which affect its trajectory and how easily it can be thrown into the hoop. The game ends when the time runs out, and the score is displayed on the screen. The challenge is to beat your high score each time you play.

## Game Mechanics
There are four shooting positions, with the first being the closest to the hoop and the fourth being the farthest away. At the beginning of the game, the player is positioned at the first shooting position, with three fruits in play: lemon, raspberry, and watermelon. The player starts by throwing the lemon and can only switch to another fruit after the lemon has been thrown successfully into the hoop. Once all three fruits have been thrown successfully, the player moves to the second shooting position and a new fruit (pineapple) is added to the mix. This pattern continues until all the fruits have been added to the game.

## Code Description
The code includes a main Pygame loop, a single class, and various functions used during the Pygame loop. Main functions are `calcul_trajectoire()`, which calculates the trajectory of the fruits, and `load_image()`, which loads the images for each position and level, including the corresponding masses and points for each fruit.

The code's main part is the Pygame loop, which calls these functions defined beforehand.

## Additional Features
The game is complete and meets all requirements specified in the project brief. Additionally, a background music that plays throughout the entire game, as well as sound effects have been added. When Kobe scores a basket, an American commentator can be heard exclaiming with excitement. To prevent the sound effect from becoming too repetitive, the random module to play the sound with a probability of 1/3 for each basket scored has been added.

When Kobe moves to level 2 or 3, a buzzer sound is played. If the high score is achieved and surpassed, an image that reads "New High Score" is displayed at the end of the game.
