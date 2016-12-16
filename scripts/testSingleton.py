from mawie.helpers import Singleton

class A(metaclass=Singleton):pass
class B(metaclass=Singleton):pass

class C():
    a = A()
    b = B()
    def __init__(self):
        print(self.a)
        print(self.b)
        print()

class D():
    __instance = None
    started = False
    def __new__(cls, *arg, **kwargs):
        if D.__instance is None:
            D.__instance = object.__new__(cls)
            print("creating new class D")
        else:
            print("class already initialised")
        print(D.__instance.started)
        return D.__instance
    def __init__(self):
        self.started = True

class X():
    d = D()
    # def __str__(self):
    #     return "Class D is  " + "started" if self.started else "not initialised"
print(D())
print(X().d.started)