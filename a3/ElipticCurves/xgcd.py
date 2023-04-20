import prettytable
import sys

#iteritive solution to xgcd
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

a = int(sys.argv[1])
b = int(sys.argv[2])

print(ixgcd(a, b))