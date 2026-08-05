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
