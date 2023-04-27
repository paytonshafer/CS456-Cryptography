import hashlib
import hmac
from datetime import datetime as dt

class DRBG():
    def __init__(self, seed):
        self.key = b'\x00' * 64
        self.val = b'\x01' * 64
        self.newseed(seed)

    def hmac(self, key, val):
        return hmac.new(key, val, hashlib.sha3_512).digest() #use hmac to haah (sha3) a new digest for the value

    def newseed(self, data=b''):
        self.key = self.hmac(self.key, self.val + b'\x00' + data)
        self.val = self.hmac(self.key, self.val)

        if data:
            self.key = self.hmac(self.key, self.val + b'\x01' + data)
            self.val = self.hmac(self.key, self.val)

    def generate(self, n):
        out = b''
        while len(out) < n:
            self.val = self.hmac(self.key, self.val)
            out += self.val

        self.newseed()

        return out[:n]
    
seed = input('Please input a seed for the deterministic random bit generator or press enter to use the current time: ')
if seed == '':
    seed = str(dt.now())
length = int(input('Please enter the number of bytes you want: '))
rand = DRBG(seed.encode())

print(rand.generate(length))