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
    a = A()
    b = B()
    def __init__(self):
        print(self.a)
        print(self.b)
        print()

print(A())
print(B())
print(C())
print(D())