# Wednesware Helium

Game and project creation library.

# Usage

## Handlers

* There are several handlers you can use to access your project files, including `script`, `res`, `lib` and `mod`.

### `ScriptHandler`

* Accessed via `project.script.<script_name>`
* Script files must end in `.py` and the script function must have the same name as the file (without extension).
* Only functions are supported for scripts.
* Passes the `project` object to the script function automatically as the first argument.
* `project.script.myCoolScript()` -> `project/scripts/myCoolScript.py:def myCoolScript(project)`

### `ResourceHandler`

* Accessed via `project.res.<resource_name>`
* Resource files must end in `.py` and the resource class must have the same name as the file (without extension).
* only classes are supported for resources.
* Does not pass the `project` object to the resource class automatically.
* `project.res.myCoolResource` -> `project/resources/myCoolResource.py:class myCoolResource`

### `LibraryHandler`
* Accessed via `project.lib.<library_name>`
* Library files must end in `.py`.
* Instead of returning an object like a function or a class, the `LibraryHandler` returns the Python module itself, so you can access any function or class within the module as you want.
* `project.lib.myCoolLibrary.myCoolFunction()` -> `project/libraries/myCoolLibrary.py:def myCoolFunction()`

## Getters

* Normally, you would use `.` to access loaders, like `project.script.my.new.script`
* However, there are alternatives to this approach that each do different things

### `getFirst()`

* Returns the first attribute.
* `project.script.getFirst().getFirst().getFirst()`

### `getFirstMatching(pattern: str)`

* Returns the first attribute that matches the given pattern.
* The pattern supports wildcards with `*` anywhere in the string.
* `project.script.getFirstMatching("my").getFirstMatching("*e*").getFirstMatching("scri*")`
* `getFirstMatching("*")` is also allowed, but `getFirst()` is preferred in this case.

### `getRandom()`

* Returns a random attribute.
* `project.script.getRandom().getRandom().getRandom()`

### `getRandomMatching(pattern: str)`

* Returns a random attribute that matches the given pattern.
* The pattern supports wildcards with `*` anywhere in the string.
* `project.script.getRandomMatching("my").getRandomMatching("*e*").getRandomMatching("scri*")`
* `getRandomMatching("*")` is also allowed, but `getRandom()` is preferred in this case.

### `getClosestMatching(pattern: str)`

* Uses an algorithm to find the closest matching attribute to the given pattern.
* **Always** returns an attribute, even if it is not a close match.
* `project.script.getClosestMatching("my").getClosestMatching("nwe").getClosestMatching("sc")`

### `getFirstPassing(condition: callable)`

* Returns the first attribute that satisfies the given condition.
* The condition should be a callable that takes an attribute as an argument and returns a boolean.
* `project.script.getFirstPassing(lambda x: x.startswith("my"))`

## File Structure

* myproject/ (your project directory)
  * settings.pyon (project settings file, uses Magnesium PYON)
  * resources/ (your project resources directory)
    * TestClass.py (a test class resource)
  * scripts/ (your project scripts directory)
    * IntegerScripts/ (a sub-directory, can be called anything that is valid as a Python identifier)
      * GetNumber.py (a number generator script)
  * libraries/ (your project libraries directory)
    * ww/ (a sub-directory, can be called anything that is valid as a Python identifier)
      * mg26_11/ (a sub-directory, can be called anything that is valid as a Python identifier)
        * logging.py (example logging module)
* main.py

Note: Nitrogen 26.41 (and after) supports the `getlib` command, which installs publications directly into `<project>/libraries/ww/`. Additionally, the same releases support the `updlibs` command, which reinstalls publications in `<project>/libraries/ww/`. For more information, see the [Nitrogen documentation](https://github.com/Wednesware/Nitrogen/blob/main/README.md).

main.py:
```
from helium import Project


project: Project = Project(__file__, "myproject") # first arg: always __file__, second arg: name of the directory to host your project in

GetNumber: callable = project.script.IntegerScripts.GetNumber # automatically returns the GetNumber function
number: int = GetNumber() # example: 3

test_object: project.res.TestClass = project.res.TestClass() # creates an instance of TestClass

mg = project.lib.ww.getFirstMatching("mg*")
info = mg.logging.info

info(test_object.s) # outputs 'this is a test'

```
myproject/settings.pyon
```
{
    "alwaysReturn10": False
}
```
myproject/scripts/IntegerScripts/GetNumber.py:
```
import random


def GetNumber(project) -> int:
  if project.getsetting("alwaysReturn10"):
      return 10
  else:
      return random.randint(1, 10)
```
myproject/resources/TestClass.py:
```
class TestClass:
    def __init__(self) -> None:
        self.s: str = "this is a test"
```
myproject/libraries/ww/mg26_11/logging.py:
```
def info(s: str) -> None:
    print(s)
```