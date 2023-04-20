from Crypto.Cipher import AES

key = 'ABCDEFHIJKLMNOPQ'.encode()
cipher = AES.new(key, AES.MODE_EAX)

data = 'Hello world'.encode()

nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)

print(key)
print(data)
print(nonce)
print(ciphertext)
print(tag)

test = nonce + b',' + ciphertext

print(test.split(b','))



cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("The message is authentic:", plaintext.decode())
except ValueError:
    print("Key incorrect or message corrupted")


cipher = AES.new(key, AES.MODE_EAX)
data = 'Goodbye world'.encode()
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)

print(key)
print(data)
print(nonce)
print(ciphertext)
print(tag)

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("The message is authentic:", plaintext.decode())
except ValueError:
    print("Key incorrect or message corrupted")

