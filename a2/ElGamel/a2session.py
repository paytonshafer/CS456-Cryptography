#vanilla elgamel
class Mod:
    def __init__(self, v, m):
        self.val = v
        self.mod = m

    def __str__(self):
        return str(self.val) + ' (mod ' + str(self.mod) + ')'

    def __add__(self, obj):
        if isinstance(obj, Zero):
            return self
        else:
            return Mod((self.val + obj.val) % self.mod, self.mod)
    
    def __floordiv__ (self, obj):
        if isinstance(obj, Zero):
            raise Exception('Error: cannot divide by 0')
        else:
            return Mod((self.val // obj.val) % self.mod, self.mod)
    
    def __mul__ (self, obj):
        return Mod((self.val * obj.val) % self.mod, self.mod)
    
    def __neg__ (self):
        return Mod((self.mod - self.val), self.mod)
    
class Zero(Mod):
    def __init__(self, m):
        self.val = 0
        self.mod = m

    def __add__(self, obj):
        return obj
    
def main():
    a = Mod(2,11)
    print(a)
    b = Zero(11)
    print(b)
    c = a + b
    print(c)

if __name__ == "__main__":
    main()