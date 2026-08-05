# Modmancer

**IMPORTANT: Modmancer is a separate product that now ships exclusively with Helium 26.18+ for convenience.**

# Nitrogen Support

Nitrogen 26.42+ includes Modmancer support in the form of a `build` format. To quickly build a `.modm` mod file from a directory, you can run `n2 build modm <mod_directory>`. This will create a `build.modm` file in the current working directory (unless result path specified).

# Mod Format

A mod is a directory (packaged as a `.modm` file, a gzipped tar archive) placed in a project's
`mods/` folder. Helium loads every `*.modm` file it finds there, in alphabetical order, when
`Modmancer(project).start()` is called.

The mod root is the directory containing `modmancer.pyon` (Helium walks the extracted archive
to find it, so the `.modm` can wrap its contents in an extra folder if desired). A typical mod
directory looks like:

```
mymod/
    modmancer.pyon    # metadata (required for author/target checks)
    __mod__.py        # optional entrypoint, run once on load
    MODINFO.md         # optional, human-readable info (not read by Helium)
    LICENSE.md          # optional
    .nitrodep           # optional, marker file for Nitrogen dependency resolution
    scripts/
        say_hello.py    # overlay patching project.script.say_hello
```

`modmancer.pyon`, `__mod__.py`, `MODINFO.md`, `LICENSE.md`, and `.nitrodep` are reserved
filenames and are never treated as overlay files.

## `modmancer.pyon`

Written in Magnesium's PYON (Python Object Notation) format. Describes the mod and which
projects it applies to:

```pyon
{
    "mod": {
        "displayName": "CoolMod",
        "version": "26.1",
        "description": "very cool mod"
    },
    "authors": [{
        "displayName": "coolmodmaker",
        "contact": {
            "email": "coolmodmaker@coolmail.com",
            "github": "https://github.com/.coolmodmaker",
            "discord": "coolmodmaker",
            "coolsocial": "coolmodmaker"
        }
    }],
    "for": "mygame"
}
```

The top-level `for` field is a glob pattern (default `"*"`) matched against the loading
project's name (`fnmatch`). If it doesn't match, the mod is skipped. If `modmancer.pyon` is
missing entirely, the mod is always applied.

## `.nitrodep`

If present, Helium runs `n2 getdep <mod_root>` before loading the mod, letting Nitrogen resolve
the mod's dependencies. If `n2` isn't installed, this step is silently skipped.

## `__mod__.py`

An optional entrypoint executed once when the mod loads, with `project` available as a module
attribute:

```python
print(f"[coolmod] loaded for {project.name}")
```

## Overlay files

Any other `.py` file in the mod is an *overlay*: it patches a matching handler module in the
project (matched by path, relative to the mod root, without the `.py` extension — e.g.
`scripts/say_hello.py` patches `project.script.say_hello`). Overlays don't define real
functions; instead, they use decorators to register hooks against functions of the same name
in the target module:

```python
@before
def say_hello(project):
    print("happens before say_hello")

@after
def say_hello(project):
    print("happens after say_hello")

@replace
def say_hello(project):
    print("hi world")

@syncwith
def say_hello(project):
    print("syncwith say_hello ran")
```

Available decorators:

- `@before` — runs before the original (or replaced) function, in registration order.
- `@after` — runs after it, in registration order.
- `@replace` — replaces the original function's body. If multiple mods replace the same
  function, the last one loaded wins.
- `@syncwith` — runs concurrently in its own thread, started before `before` hooks and joined
  after `after` hooks complete.
- `@delete` — makes calling the function raise `ModmancerError` instead of running it. Takes
  precedence over all other decorators for that function.

Multiple mods can patch the same function; hooks from all of them accumulate and run in load
order.

### Classes

Overlay files may also define classes matching a class in the target module, in which case the
same decorators can be used on methods inside the class body to patch that class's methods:

```python
class Greeter:
    @before
    def say_hello(self):
        print("happens before Greeter.say_hello")

    @replace
    def say_hi(self):
        print("hi!")
```

Classes can be nested to reach nested classes in the target module — a `class Inner:` defined
inside a `class Outer:` overlay patches `target_module.Outer.Inner`, to any depth.

The class itself can also be decorated with `@before`, `@after`, `@replace`, or `@delete`,
which patches its construction (i.e. calling `Greeter(...)`) the same way a function call would
be patched. `@syncwith` isn't supported on classes and raises a `ModmancerError` if used.

```python
@before
class Greeter:
    @replace
    def say_hi(self):
        print("hi!")
```