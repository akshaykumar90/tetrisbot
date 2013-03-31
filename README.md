Tetris Bot
==========

A bot to play the online tetris flash game at [freetetris.org](http://www.freetetris.org/data/flash/nbloxFreeTetris.swf)

The coordinates for the positions of play game button, next block and current block are hard-coded in gamedata.py.

The bot uses a very basic AI for now - mostly brute-forcing its way to complete line after line. All in all, not very good yet but will be improved upon in future.

There are intermittent issues with the bot losing sync with the game. This may happen due to delay in screen transition, missed keystrokes etc. which confuses the bot and results in a messed-up game.

The aim is to try different playing strategies and improve the level, high score and lines completed over time.
