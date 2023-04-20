#python3 rsa_decrypt.py sec.keys encrypt.txt decrypt.txt to run
import sys

keys = open(sys.argv[1], 'r') #secret key file
encrypt = open(sys.argv[2], 'r') #encytped file to be decrypted
decrypt = open(sys.argv[3], 'w') #file to output decrypted message

N = int(keys.readline()) #modulus n
d = int(keys.readline()) #secret exponent

text = encrypt.readlines()

for i in text:
    decrypt.write(chr(pow(int(i), d, N)))