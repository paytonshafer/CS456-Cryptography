'''
Client                 Server
    <----(pubkeys)---  EG
AES 
s   ------ EG(s) --->  s

Client uses server RSA/Elgamel to send AES sec key to server
So now both just use AES sec key to communicate
'''
from elgamel_gen_keys import main
from elgamel_decrypt import elgamel_decrypt
from Crypto.Cipher import AES
import socket
import threading

def set_up_elgamel():
    bitlen = input('Please enter the desired bit length for your El-Gamel primes: ')
    print('Setting up El-Gemal keys ...')
    return main(int(bitlen), 100)

class ServerNode:
    def __init__(self):
        self.EGkeys = set_up_elgamel()
        print('\nwaiting for client connection ...')
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_and_ip = ('127.0.0.1', 12345)
        self.node.bind(port_and_ip)
        self.node.listen(5)
        self.connection, addr = self.node.accept()
        self.secure = False
        self.AESkey = ''

    def receive_sms(self):
        while True:
            if self.secure:
                data = self.connection.recv(1024)
                [nonce, ciphertext, tag] = data.split(b':')
                
                cipher = AES.new(self.AESkey.encode(), AES.MODE_EAX, nonce=nonce)
                plaintext = cipher.decrypt(ciphertext)
                print('<received ciphertext from client:', ciphertext, '>') if plaintext.decode() != 'exit()' else None
                print('<decrypting ...>') if plaintext.decode() != 'exit()' else None
                if plaintext.decode() == 'exit()':
                    print('<the client exited>')
                    exit()
                print('<client> ' + plaintext.decode() + '\n')
            else:
                encrypted_key = self.connection.recv(1024).decode().split('\n')[:-1]
                self.AESkey = elgamel_decrypt(self.EGkeys[0], self.EGkeys[3], encrypted_key)
                #print(self.AESkey)
                self.secure = True
                print('<received AES secret key from client: ' + self.AESkey + '>')
                print('<secure connection completed, type exit() to quit>')


    def main(self):
        print('<sending client public keys>')
        self.connection.send((str(self.EGkeys[0]) + ',' + str(self.EGkeys[1]) + ',' + str(self.EGkeys[2])).encode()) #send pub keys to client
        while True:
            message = input()
            print('<encrypting ...>') if message != 'exit()' else None
            cipher = AES.new(self.AESkey.encode(), AES.MODE_EAX)
            data = message.encode()
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            print('<sending ciphertext to client:', ciphertext, '>\n') if message != 'exit()' else None
            to_send = nonce + b':' + ciphertext + b':' + tag
            self.connection.send(to_send)
            if message == 'exit()':
                exit()

server = ServerNode()
always_receive = threading.Thread(target=server.receive_sms)
always_receive.daemon = True
always_receive.start()
server.main()