#python3 rsa_gen_keys.py bitlength 100 sec.keys pub.keys to run  
import sys
from random import randint

def main():
    #get from system args: bit length, confidence, and key files(public and secret)
    bitlength = int(sys.argv[1])
    confidence = int(sys.argv[2])
    sec = open(sys.argv[3], 'w')
    pub = open(sys.argv[4], 'w')

    keys = genRSAkeys(bitlength, confidence) #generate the keys

    pub.write(str(keys[2]) + '\n') #Modulo n
    pub.write(str(keys[4])) #public exp e
    sec.write(str(keys[2]) + '\n') #Modulo n
    sec.write(str(keys[5])) #secrect exp d

    print("p =", keys[0])
    print("q =", keys[1])
    print("n =", keys[2])
    print("phi =", keys[3])
    print("e =", keys[4])    
    print("d =", keys[5])

    print("sanity check: e*d (mod phi) =", (keys[4]*keys[5])%keys[3], "= 1 (mod phi)")
    


def genRSAkeys(bitlength, confidence):
    #low and hi bounds for p and q
    lo = pow(2, bitlength-1)
    hi = pow(2, bitlength)-1


    #generate p
    while True:
        p = randint(lo,hi)
        if isPrime(p, confidence):
            break

    #generate q
    while True:
        q = randint(lo,hi)
        if (q != p and isPrime(q, confidence)):
            break

    n = p*q #get module n
    phi = (p-1)*(q-1) #get phi

    #below to find e and d, e will be the smalled odd int that works
    e = 3
    d = 0
    while True:
        #below returns [D,x,y] such that D = gcd(a,b) =  ax + by
        ans = ixgcd(phi, e) #iterative algorithm of xgcd
        if ans[0] == 1:
            d = ans[2]
            while d < 0: #rounding d module phi such that d is positive
                d = d + phi
            break
        e = e + 2

    return [p,q,n,phi,e,d]


def isPrime(m,k):
    for _ in range(k):
        a = randint(1, m-1)
        if not(expmod(a,m,m) == a): #note, to do larger numbers(more bits for p and q) do pow instead of expmod(around 65 bits)
            return False               #but, pow does NOT have the raben test so using it may give wrong answers
    return True

#Just a recursive algorithm for expmod
def expmod(a, b, m): #this funcion will take superrrrr long if a and b are large
    if b == 0:
        return 1
    elif b%2 == 0: #b is even
        y = expmod(a, b/2, m)
        z = (y*y)%m
        if z == 1 and not(y == (m-1) or y == 1):
           return 0
        return z
    else: #b is odd
        y = expmod(a, b-1, m)
        z = (a*y)%m
        return z

#This is the tail recursive version of expmod but the below 
#does not have the raben test yet so it will not work (carmicheal numbers will trick this)
def expmod_tr(a, b, m, acc=1):
    if b == 0:
        return acc
    elif b % 2 == 0:  # b is even
        #two lines below are what i wrote before adding raben test
        y = (a * a) % m
        return expmod_tr(y, b // 2, m, acc)
    else:  # b is odd
        z = (a * acc) % m
        return expmod_tr(a, b - 1, m, z)
    
#purely recursive xgcd function
def rxgcd(a, b):
    if (a < b):
        ans = rxgcd(b, a)
        return [ans[0], ans[2], ans[1]]
    else:
        if (b == 0):
            return [a, 1, 0]
        else:
            q = a//b #a = qb + r
            r = a%b
            ans = rxgcd(b, r) #returns [d, x', y']
            return [ans[0], ans[2], (ans[1] - q*ans[2])] #turn ans into [d, y', x' - q*y']
            
#iteritive solution to xgcd
def ixgcd(a,b):
    if a < b: #this is just to ensure that the algorithm returns the ans in the right order
        ans = ixgcd(b, a)
        return [ans[0], ans[2], ans[1]]
    
    x1 = 1
    y1 = 0
    x2 = 0
    y2 = 1

    while b != 0:
        q = a // b
        r = a % b

        a = b
        b = r
        newx2 = x1 - q*x2
        newy2 = y1 - q*y2
        x1 = x2
        y1 = y2
        x2 = newx2
        y2 = newy2

        #print(a,b,q,r,x1,y1,x2,y2)

    return [a, x1, y1]

if __name__ == '__main__':
    #main()
    print(ixgcd(47,11))
