# CS456-Cryptography
This repository contains all of my assignments from CS456: Cryptography at Clarkson Univeristy in spring 2023. Assignment 1 through 3 required you to 
break a given file using the information that was given and then usually something extra. All of my solutions are done in python. The Chat-Protocal is an 
exrypted chat protocal that allows two parties to conduct secure communication, this was also done in python.

## SHA-3
Examining SHA-3 was for the final project for this class. We were assigned to do a research project on an area in cyrptography and I chose to do SHA-3. We were assigned a 5-10 page paper on it and a 5-10 minute presentaion. First look at sha3.py, this is my implementation of SHA-3 in python. To run the program cd into the SHA-3 directory and run:
```sh
python3 sha3.py
```
After this you will be prompted to chose the version of sha-3 which conists of 224, 256, 384, 512 and these dertimine the bit length of the output digest. Once you have chosen a version you will be prompted to enter the data you would like hashed. After that the data is hashed and the hex digest is printed out. Next there is a file named sha3libraries.py, this file contains the 4 main sha3 functions, sha3 on a file (showing how after 'corrupting' a file you get a differnt hash), SHAKE (an extendable output function that allows you to choose the number of bits as output), and KangarooTwelve which is a derivation oh SHA3 which is intended to be faster. To run this program type:
```sh
python3 sha3libraries.py
```
After you run it the program will take you through each of the algorithms so that you can see what the hashed data will look like. Lastly, the file drbg.py is my version of a deterministic random bit generator using keyed-hashing for message authentication and SHA3_512 to create a requested number of random bytes and outputting them. To run this run:
```sh
python3 drbg.py
```
After running this you will be prompted to create a seed for the generator then you will be asked for a number of random bytes you would like. To exit you must simple enter 0 and to reseed the generator you must enter 999.

## a1
This assignment's topic was RSA. The first thing I had to do was break the file cipher.txt in hacka1. I did this by encoding every ascii character with
the public keys that we were given and then compared them to the cipher text and printed the plaintext to broken.txt. To see how this was done please 
look at hacka1.py in hacka1. Once broken, the cipher text stated that I had to implement an RSA crypto-system which can be found in the RSA directory. 
The RSA implementation consists of 3 files: rsa_gen_keys.py, rsa_encrypt.py, and rsa_decrypt.py. The first one, rsa_gen_keys.py, takes the desired prime
bit-length, the desired confidence interval, the file to write the secret keys and a file to write the public keys. An example is shown below where you
would input your own values for each of the arguments:
```sh
python3 rsa_gen_keys.py bitlength sec.keys pub.keys
```
Next to encrypt a file, use rsa_encrypt.py which takes the public keys file, the file with the plain text and a file for the encryption to go. An example 
is shown below where you would input your own values for each of the arguments:
```sh
python3 rsa_encrypt.py pub.keys plain.txt encrypt.txt
```
Lastly, to decrypt a file use rsa_decrypt.py which takes the secret key file, the encrypted text file, and a file to write the decrytion to.
An example is shown below where you would input your own values for each of the arguments:
```sh
python3 rsa_decrypt.py sec.keys encrypt.txt decrypt.txt
```

## a2
This assignments topic was the ElGamel public key cryptosystem. I was given all of the public keys and not the secret key to break the cipher. To get the 
secret key you had to break assignment 3 which was encrypted using ElGamel with eliptic curves. Once I got the secret keys I broke the cipher text using
hack.py in the hacka2 directory. After breaking the assignment I was given the description for the chat-protocal. I also created a ElGamel system
in python. The implementation consists of 3 files: elgamel_gen_keys.py, elgamel_encrypt.py, and elgamel_decrypt.py. The first one, elgamel_gen_keys.py, takes the desired prime
bit-length, the desired confidence interval, the file to write the secret keys and a file to write the public keys. An example is shown below where you
would input your own values for each of the arguments:
```sh
python3 elgamel_gen_keys.py bitlength sec.keys pub.keys
```
Next to encrypt a file, use elgamel_encrypt.py which takes the public keys file, the file with the plain text and a file for the encryption to go. An example 
is shown below where you would input your own values for each of the arguments:
```sh
python3 elgamel_encrypt.py pub.keys plain.txt encrypt.txt
```
Lastly, to decrypt a file use elgamel_decrypt.py which takes the public keys, the secret key file, the encrypted text file, and a file to write the decrytion to.
An example is shown below where you would input your own values for each of the arguments:
```sh
python3 elgamel_decrypt.py pub.keys sec.keys encrypt.txt decrypt.txt
```

## a3
This assignment was baed on ElGamel with eliptic curves. Here I was given a cipher and all of the keys to decrypt it. I decrypted it using the file hacka3.py
in the hacka3 directory which has adding over elptic curves implemented. In the folder ElipticCurves there are two python files: xgcd.py and ecadd.py which
are designed to be helper functions for this. xgcd.py contains the Extented Euclidean Algorithm (The Pulverizer), which takes it's arguments from the command
line and prints out a complete table as well as the solution. To run it simply use this command with num1 and num2 as your inputs.
```sh
python3 xgcd.py num1 num2
```
The other file, ecadd.py, is a file which allows you to add two points on an eliptic curve. The inputs are also taken from the command line; this function
takes: [x1, y1] (first point), [x2, y2] (second point), the prime, and the A value from the equation. Simply run this command with your arguemnts:
```sh
python3 ecadd.py x1 y1 x2 y2 prime A
```


## Chat-Protocal
The final assignment was to create an encrypted chat protocal that uses RSA or ElGamel to send a secret key then uses that secret key with AES/DES for
encrypting the messages. I chose to use ElGamel and AES in my implementation, which I did in python using the socket module. I used my own implementation
for ElGamel and I used the Crypto.Cipher package for AES. All the connections are hard coded and currently they are hard coded to all be local, but this will work over a network.
To run the program you need to start the server first by running:
```sh
python3 server.py
```
Once the server has been started you will be prompted to pick your prime bit-length and then the server waits for a client connection to send the
public keys to. So now you have to start the client by opening a new terminal window and running:
```sh
python3 client.py
```
One the client starts you will be prompted to enter your AES secret which has to be 16 characters. Once that is selected the client uses the server's
public keys to encrypt the AES key and send it to the server to decrypt. Once both the server and client have the AES key, the channel is secure and you
are free to chat back and forth since every message is encrypted with AES before it is sent.