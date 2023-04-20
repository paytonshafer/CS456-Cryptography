from random import randint

def main(bitlength, confidence):
    keys = genRSAkeys(bitlength, confidence) #generate the keys

    print("p =", keys[0])
    print("g =", keys[1])
    print("b =", keys[2])
    print("a =", keys[3])

    return keys
    


def genRSAkeys(bitlength, confidence):
    #low and hi bounds for p and q
    lo = pow(2, bitlength-1) // 2
    hi = (pow(2, bitlength)-1) // 2


    #generate p
    while True:
        q = randint(lo,hi)
        if isPrime(q, confidence):
            p = 2*q + 1
            if isPrime(p, confidence):
                break


    #generate g
    while True:
        g = randint(1, p-1)
        if isGenerator(g,p):
            break
    
    #get a
    a = randint(0, p-1)

    #calculate b
    b = expmod(g, a, p)

    return [p,g,b,a]


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
    
def isGenerator(g, p):
    q = (p-1)//2
    if (g % p == 1) or (pow(g,2,p) == 1) or (pow(g,q,p) == 1):
        return False
    
    return True

if __name__ == '__main__':
    main(20, 100)
