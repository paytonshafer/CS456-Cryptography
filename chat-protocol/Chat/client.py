from elgamel_encrypt import elgamel_encrypt
from Crypto.Cipher import AES
import socket 
import threading

def get_AES_key():
    while True:
        key = input('Please input your 128 bit(16 char) secret key for AES:\n')
        if len(key) == 16:
            break
        else:
            print('Please ensure that your AES key is 16 characters(128 bits)\n')

    return key

class ClientNode:
    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_and_ip = ('127.0.0.1', 12345)
        self.AESkey = get_AES_key()
        #print(self.AESkey)
        self.node.connect(port_and_ip)
        self.EGkeys = []

    def send_sms(self, SMS):
        self.node.send(SMS.encode())
    
    def send_encrypted_key(self):
        self.EGkeys = self.node.recv(1024).decode().split(',')
        print('<received public keys from server>')
        self.send_sms(elgamel_encrypt(int(self.EGkeys[0]), int(self.EGkeys[1]), int(self.EGkeys[2]), self.AESkey))
        print('<sending server encrypted AES secret key>')
        print('<secure connection completed, type exit() to quit>')

    def receive_sms(self):
        self.send_encrypted_key()
        while True:       
            data = self.node.recv(1024)
            [nonce, ciphertext, tag] = data.split(b':')
            
            cipher = AES.new(self.AESkey.encode(), AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            print('<received ciphertext from server:', ciphertext, '>') if plaintext.decode() != 'exit()' else None
            print('<decrypting ...>') if plaintext.decode() != 'exit()' else None
            if plaintext.decode() == 'exit()':
                print('<the server exited>')
                exit()
            print('<server> ' + plaintext.decode() + '\n')

    def main(self):
        while True:
            message = input()
            print('<encrypting ...>') if message != 'exit()' else None
            cipher = AES.new(self.AESkey.encode(), AES.MODE_EAX)
            data = message.encode()
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            print('<sending ciphertext to server:', ciphertext, '>\n') if message != 'exit()' else None
            to_send = nonce + b':' + ciphertext + b':' + tag
            self.node.send(to_send)
            if message == 'exit()':
                exit()

        

Client = ClientNode()
always_receive = threading.Thread(target=Client.receive_sms)
always_receive.daemon = True
always_receive.start()
Client.main()