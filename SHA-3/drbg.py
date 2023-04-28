import hashlib #to get sha3_512
import hmac #this lets us create hashes for a value from a key
from datetime import datetime as dt #get this for the current time

#the class the create random bits
class DRBG():
    #we only take the see as input 
    def __init__(self, seed):
        self.key = b'\x00' * 64 #this is a standardized value
        self.value = b'\x01' * 64 #this is a standardized value
        self.newseed(seed) #this is create a key and value from the seed

    #here we create our hmac object and immediately get the digest based on the key and value
    def hmac(self, key, value):
        return hmac.new(key, value, hashlib.sha3_512).digest() #use hmac to haah (sha3) a new digest for the value

    #function to get a new seed for the next interation
    def newseed(self, data=b''):
        #the below is done on every call of this function
        self.key = self.hmac(self.key, self.value + b'\x00' + data)
        self.value = self.hmac(self.key, self.value)

        if data: #this is only done on the first iteration when we put our seed in
            self.key = self.hmac(self.key, self.value + b'\x01' + data)
            self.value = self.hmac(self.key, self.value)

    #this is the function to generate n random bytes
    def generate(self, n):
        out = b'' #inital empty byte string
        while len(out) < n: #while we are less than n
            self.value = self.hmac(self.key, self.value) #get a new rand value (byte)
            out += self.value #add the rand byte to the outpute

        self.newseed() #reset the seed after each generation

        return out[:n] #return the n byte string

#below is to get an inital seed and initalize the drbg 
seed = input('Please input a seed for the deterministic random bit generator or press enter to use the current time: ')
if seed == '':
    seed = str(dt.now())
rand = DRBG(seed.encode())

while True:
    length = int(input('Please enter the number of bytes you want, type 0 to exit, or type 999 to reseed the DRBG: '))
    if length == 0: #0 to exit
        break
    if length == 999: #999 to reseed
        seed = input('Please input a seed for the deterministic random bit generator or press enter to use the current time: ')
        if seed == '':
            seed = str(dt.now())
        rand = DRBG(seed.encode())
    else: #else print that many bits
        print(rand.generate(length))