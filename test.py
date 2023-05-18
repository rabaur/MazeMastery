class A:
    def __init__(self):
        self.counter = 0
        self.b = B(self)

class B:
    def __init__(self, a):
        self.a = a
    
    def inc(self):
        self.a.counter += 1

a = A()
a.b.inc()
print(a.counter)