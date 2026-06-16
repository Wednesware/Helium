# Wednesware Helium

Game and project creation framework.

## Usage

### File Structure

* myproject/ (your project directory)
  * settings.pyon (project settings file, uses Magnesium PYON)
  * resources/ (your project resources directory)
    * TestClass.py (a test class resource)
  * scripts/ (your project scripts directory)
    * IntegerScripts/ (a sub-directory, can be called anything that is valid as a Python identifier)
      * GetNumber.py (a number generator script)
* main.py

main.py:
```
from helium import project


myproject: project = project(__file__, "myproject") # first arg: always __file__, second arg: name of the directory to host your project in

GetNumber: callable = myproject.script.IntegerScripts.GetNumber # automatically returns the GetNumber function
number: int = GetNumber() # example: 3

test_object: myproject.res.TestClass = myproject.res.TestClass() # creates an instance of TestClass

print(test_object.s) # outputs 'this is a test'

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


def GetNumber(myproject) -> int:
  if myproject.getsetting("alwaysReturn10"):
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
