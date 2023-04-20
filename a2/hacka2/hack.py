#python3 hack.py a2.pubkeys.txt seckeys.txt a2.cipher.txt broken.txt to run
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

pubkeys = open(sys.argv[1], 'r') #public key file
seckeys = open(sys.argv[2], 'r') #secret key file
encrypt = open(sys.argv[3], 'r') #encytped file to be decrypted
decrypt = open(sys.argv[4], 'w') #file to output decrypted message

p = int(pubkeys.readline()) #prime p
a = int(seckeys.readline()) #secret value

text = encrypt.readlines() #read all cipher text

for i in text:
    [h,c] = i.split(',') #get cipher text and half mask

    f = pow(int(h),a,p) #calcualate full mask

    f_inv = (ixgcd(p,f)[2]) % p #calculate full mask inverse

    m = (int(c) * f_inv) % p #decrpyt the message

    decrypt.write(chr(m)) #write message to file
