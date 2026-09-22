[![Wednesware](wednesware.png)](https://wednesware.org)

# Helium

Game and project creation library.

## Installation

> `n2 get helium`

## Quick start

### Example usage 1: basic project setup

```python
from helium import Project

project: Project = Project(__file__, "mygame")
project.script.say_hello()
```

### Example usage 2: calling a script function from a nested folder

```python
from helium import Project

project: Project = Project(__file__, "mygame")

GetNumber = project.script.IntegerScripts.GetNumber
number = GetNumber()
print(number)
```

### Example usage 3: loading a resource and reading settings

```python
from helium import Project

project: Project = Project(__file__, "mygame")

value = project.getsetting("alwaysReturn10", False)
item = project.res.TestClass()
print(value)
print(item.s)
```

## Dependencies

- Python 3.12+
- Nitrogen 26.62+ (`pip install wwn`)

# Definitions

## `helium`

From the base library, you can import `Project` and related project loaders.

> `from helium import Project, ScriptHandler, ResourceHandler, ModHandler, main`

### `helium:Project(path: str, name: str)`

**For the `path` parameter, always provide `__file__`**. Creates a project wrapper for the directory named `name`, resolved relative to the file path passed in `path`. The `Project` object exposes handlers for scripts, resources, and mods in the project root.

> `project = Project(__file__, "mygame")`

#### `helium:Project.getsetting(name: str, else_value: any = "<raiseerror>", scope: str = "prefer args", arg_names: list[str] | None = None) -> any`

Reads a setting from either CLI arguments or the project's `settings.pyon` file.

- `scope="prefer args"`: use the CLI value if present, otherwise fall back to settings.
- `scope="only args"`: read only command-line arguments.
- `scope="only settings"`: read only the settings file.
- `scope="return both"`: return both the CLI and settings values.
- `scope="return none"`: return `None` if no value is found.

> `value = project.getsetting("alwaysReturn10", False)`
>
> `username = project.getsetting("username", scope="only args")`

### `helium:ScriptHandler`

Accessed via `project.script.<script_name>`. Script files must live under the project's `scripts/` directory and end in `.py`. The function name must match the filename, and the project instance is passed in automatically as the first argument.

> `project.script.say_hello()`
>
> `project.script.IntegerScripts.GetNumber()`

#### `helium:ScriptHandler.getFirst()`

Returns the first script or script folder entry found in the `scripts/` directory.

> `project.script.getFirst()`

#### `helium:ScriptHandler.getFirstMatching(pattern: str)`

Returns the first script that matches the provided wildcard pattern. `*` can be used anywhere in the query.

> `project.script.getFirstMatching("my*")`
>
> `project.script.getFirstMatching("*hello*")`

#### `helium:ScriptHandler.getRandom()`

Returns a random script entry from the `scripts/` directory.

> `project.script.getRandom()`

#### `helium:ScriptHandler.getRandomMatching(pattern: str)`

Returns a random script whose name matches the pattern.

> `project.script.getRandomMatching("*e*")`

#### `helium:ScriptHandler.getClosestMatching(pattern: str)`

Returns the closest file name match using a similarity algorithm.

> `project.script.getClosestMatching("scr")`

### `helium:ResourceHandler`

Accessed via `project.res.<resource_name>`. Resource files must contain a Python class whose class name matches the filename. The class is returned directly, and the project object is not automatically injected.

> `item = project.res.TestClass()`
>
> `item = project.res.testsubfolder.TestResource()`

### `helium:ModHandler`

Accessed via `project.mod.<mod_name>`. Mods are loaded from the project's `mods/` directory and may be packaged as `.modm` archives. Mod patches are applied by `Modmancer`.

> `project.mod.getFirstMatching("*")`

### `helium:main(path: str)`

**For the `path` parameter, always provide `__file__`**. Used to provide a CLI entrypoint to a project. Within your project's base directory, create a `__main__.py` file with the following contents:

```python
from nitrogen import require
require("helium").main(__file__)
```

The above code handles commands such as `python -m project`. `main` itself creates `Project` instance at `.` relative to the `__file__` provided, then runs the `main` script found within it (`project/scripts/main.py:main`). You may collect the object and the return value of the `main` script easily as follows:

> `project, result = main(__file__)`

## `modmancer`

From this library, you can manage and apply mods to your project using the `Modmancer` class.

> `from helium.modmancer import Modmancer`

### `modmancer:modmancer`

The `Modmancer` class applies runtime patches from `.modm` files. It is initialized with a `Project` and started with `.start()`. This lets mods override, wrap, or synchronize functions and classes in project modules.

> `modm = Modmancer(project)`
>
> `modm.start()`

### `modmancer:Modmancer.start()`

Loads all `.modm` archives from the project's `mods/` directory and applies their patches.

> `modm.start()`

### `modmancer:Modmancer.patch_module(relative_path: str, module: any)`

Applies any registered patch information to a loaded module at the given relative path.

> `modm.patch_module("scripts/my_script.py", script_module)`
