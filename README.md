# Memory_Match
A memory match python game, written in pygame.

The program works by having two decks: a visual deck and a hidden one. Upon game start, the visual deck is the backsides of all the cards, and the hidden deck is all the card faces. As the user finds matches, the two matching card faces from the hidden deck replace the card backs of the visual deck, thereby making them permanently visual. At the end of the game, the hidden deck becomes the visual deck - all card faces are shown. When the user restarts the game, the visual deck is reset to the card backs, and a new, randomized hidden deck is created.

This program utilizes python 2.7 and package python-pygame (http://pygame.org/).
As such, both must be installed to run.
This game has only been tested on Ubuntu 14.04.

The images are not my original creation. They were taken from http://colome.org/ and spliced to make individual cards. Because of this, this program is under no license.
