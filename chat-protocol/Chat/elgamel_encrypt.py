#python3 elgamel_encrypt.py pub.keys plain.txt encrypt.txt to run
from random import randint

def elgamel_encrypt(p, g, b, key_to_encrypt):
    encrypted_key = ''


    for i in key_to_encrypt:
        alpha = randint(0, p-1) #get alpha
        h = pow(g, alpha, p) #calculate half mask
        f = pow(b, alpha, p) #calculate full mask
        c = (ord(i)*f) % p #encrypt the char
        encrypted_key = encrypted_key + (str(c) + ',' + str(h) + '\n')

    return encrypted_key