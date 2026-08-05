from helium import Project
from helium.modmancer import Modmancer


project: Project = Project(__file__, "mygame")
modm: Modmancer = Modmancer(project)
modm.start()

project.script.say_hello()
