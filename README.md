# This is from EAI Assignment @ IUB MSCS

Game of Quintris

Idea of the game The game of Quintris starts off with a blank board. One by one, random pieces (each consisting of 5 blocks arranged in different shapes) fall from the top of the board to the bottom. As each piece falls, the player can change the shape by rotating it or flipping it horizontally, and can change its position by moving it left or right. It stops whenever it hits the ground or another fallen piece. If the piece completes an entire row, the row disappears and the player receives a point. The goal is for the player to score as many points before the board fills up.

Approach: The basic implementation of Quintris has already been given that can be played from the command line. The goal of this project is to write a computer player for this game that scores as high as possible. To do this, we need to move each falling piece to its optimal position before it hits the bottom or another piece, so that the rows keep clearing quickly. In the code, we have implemented this by first figuring out the holes, empty blocks, trenches and cleared lines, and then calculating the optimal orientation and position with the help of heuristics.

One crucial factor which helped in getting high scores: the falling pieces are not chosen uniformly at random but based on some distribution which your program is not allowed to know ahead of time. However, it may be able to learn the distribution as it plays, which may let it make better decisions over time.

The code has been executed in Python using the Linux terminal. The following command is used to run the quintris.py file.

$ python3 quintris.py computer animated
