import prettytable
import sys

def ixgcd(a,b):
    if a < b: #this is just to ensure that the algorithm returns the ans in the right order
        ans = ixgcd(b, a)
        return [ans[0], ans[2], ans[1]]
    
    x1 = 1
    y1 = 0
    x2 = 0
    y2 = 1
    x = prettytable.PrettyTable(["a", "b", 'q', 'r', 'x1', 'y1', 'x2', 'y2'])

    while b != 0:
        q = a // b
        r = a % b

        x.add_row([a, b, q, r, x1, y1, x2, y2])

        a = b
        b = r
        newx2 = x1 - q*x2
        newy2 = y1 - q*y2
        x1 = x2
        y1 = y2
        x2 = newx2
        y2 = newy2

    print(x)
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

    print(m%prime, x3, (m*x3 + c)%prime)

    result = '[' + str(x1) + ',' + str(y1) +  '] + [' + str(x2 )+ ',' + str(y2) + '] = [' + str(x3) + ',' + str(y3) +  ']'
    print(result)

    return [x3,y3]

P1 = int(sys.argv[1])
P2 = int(sys.argv[2])
Q1 = int(sys.argv[3])
Q2 = int(sys.argv[4])
prime = int(sys.argv[5])
A = int(sys.argv[6])

eliptic_curve_add([P1,P2], [Q1, Q2], prime, A)