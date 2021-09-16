class Singleton:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

class Foo(Singleton):
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    foo1 = Foo('foo')
    foo2 = Foo('foo')
    print(id(foo1))
    print(id(foo2))