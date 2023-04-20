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

    return [a, x1, y1]

#adding over an eliptic curve group
def eliptic_curve_add(P, Q, prime, A):
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]

    if P != Q:
        diff_inv = ixgcd(prime, (x2-x1)%prime )[2]

        m = (y2 - y1) * diff_inv #slope
        c = -m*x1 + y1 #y-interecept

    elif P == Q:
        y_inv = ixgcd(prime, (2*y1)%prime )[2]

        m = (3*(x1**2) + A) * y_inv #slope
        c = -m*x1 + y1 #y-interecept

    x3 = (m**2 - (x1 + x2))%prime
    y3 = (-(m*x3 + c))%prime

    return [x3,y3]

#INPUT files
cipher = open('a3.cipher.txt')
keys = open('a3.pubkeys.txt')
plain = open('plain.txt', 'w')

#get prime q
q = int(keys.readline()[8:])

#get A and B
keys.readline()
keys.readline()
A = int(keys.readline()[4:])
B = int(keys.readline()[4:])

#get generator
keys.readline()
g = keys.readline().split(',')
g[0] = int(g[0][13:])
g[1] = int(g[1][:-2])

#get public point
keys.readline()
p = keys.readline().split(',')
p[0] = int(p[0][16:])
p[1] = int(p[1][:-2])

#Secret Multiplier = smallest prime that is not the oddest one
n = 3

#print('q= ' + str(q) + '\n', 'A= ' + str(A) + '\n', 'B= ' + str(B) + '\n', 'g= ' + str(g) + '\n', 'p= ' + str(p) + '\n', 'n= ' + str(n))

#cipher text
while(1):
    T = cipher.readline().split(' ')

    if T[0] == '':
        break

    C = [int(T[0]), int(T[1])]
    H = [int(T[2]), int(T[3])]

    F = H
    for _ in range(n-1):
        F = eliptic_curve_add(F, H, q, A)

    neg_F = [F[0], (-F[1])%q]

    M = eliptic_curve_add(C, neg_F, q, A)
    plain.write(chr(M[0]))