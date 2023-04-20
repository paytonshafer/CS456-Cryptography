#python3 rsa_encrypt.py pub.keys plain.txt encrypt.txt to run
import sys

pubkeys = open(sys.argv[1], 'r') #pub key file
plain = open(sys.argv[2], 'r') #plain text to be encrypted
encrypt = open(sys.argv[3], 'w') #file to write the encrypted text to

N = int(pubkeys.readline()) #modulus n
e = int(pubkeys.readline()) #public exponent

lines = plain.readlines()
text = ''
text = text.join(lines)

for i in text:
    encrypt.write(str(pow(ord(i), e, N)) + '\n')