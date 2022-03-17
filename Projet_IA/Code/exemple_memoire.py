class A:
    def __init__(self, nom:str, x):
        self.__name = nom
        self.__toto = x

    def miam(self):
        print("{} fait miam()".format(self.__name))
        if self.jambon  == "fromage":
            self.miam.memoire[self.jambon] = "miam"
        else:
            self.miam.memoire[self.jambon] = 'burp'

    miam.memoire = {}

    @property
    def jambon(self): return self.__toto



a = A('a', 42)
b = A('b', 'fromage')
c = A('c', 'Fromage')

print('A', A.miam.memoire)
print('a', a.miam.memoire)
print('b', b.miam.memoire)
print('c', c.miam.memoire)

a.miam()

print('A', A.miam.memoire)
print('a', a.miam.memoire)
print('b', b.miam.memoire)
print('c', c.miam.memoire)

b.miam()

print('A', A.miam.memoire)
print('a', a.miam.memoire)
print('b', b.miam.memoire)
print('c', c.miam.memoire)

c.miam()

print('A', A.miam.memoire)
print('a', a.miam.memoire)
print('b', b.miam.memoire)
print('c', c.miam.memoire)
