from helium import Project

mygame: Project = Project(__file__, "mygame")
mg = mygame.lib.ww.getClosestMatching("mg")
print(mg.MESSAGE)