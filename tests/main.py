import os

from helium import *


game: Project = Project(__file__, "test_game")

print(game.getsetting("username", scope="only args"))

print(game.res.testsubfolder.TestResource.NAME)