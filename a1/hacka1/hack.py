import string

f1 = open("cipher.txt")
f2 = open("pubkeys.txt")
out = open("broken.txt", 'w')

c = f1.readlines()
N = int(f2.readline())
e = int(f2.readline())

#My idea is to encrpyt the alphabet with the public keys then compare that to the encryption
alph = list(string.printable) #gives list of evry single printable ascii character
encAlph = []
for i in alph:
    encAlph.append(pow(ord(i), e, N)) #adds the encrytion of each ascii char to the list

res = {} #the below creates a dictionary where the encrypted char is the key and the ascii char is the value
for key in encAlph:
    for value in alph:
        res[key] = value
        alph.remove(value)
        break

for i in c:
    #print(res[int(i)], end='') This is to print to standard output the below is to write it to a file
    out.write(res[int(i)])