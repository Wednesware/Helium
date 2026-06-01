import os

from helium import *


game: Game = Game(eval(CWD), "test_game")

print(game.res.testsubfolder.TestResource.NAME)