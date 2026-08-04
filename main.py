from helium import Project

mygame: Project = Project(__file__, "mygame")

mygame.script.prints.PrintInfo()
mg = mygame.lib.ww.getClosestMatching("mg")
mg.logging.error("This is an error message").print()