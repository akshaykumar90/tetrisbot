Tetris Bot
==========

A bot to play the online tetris flash game at [freetetris.org](http://www.freetetris.org/data/flash/nbloxFreeTetris.swf)

The coordinates for the positions of play game button, next block and current block are hard-coded in gamedata.py.

The bot uses a very basic AI for now. The falling blocks aim to minimize the voids created below them, and for same number of voids created, blocks with lower baseline are preferred.

There are intermittent issues with the bot losing sync with the game. This may happen due to delay in screen transition, missed keystrokes etc. which confuses the bot and results in a messed-up game.

The aim is to try different playing strategies and improve the level, high score and lines completed over time.

Current highest - Level 12 - 113 Lines - Score 63283
