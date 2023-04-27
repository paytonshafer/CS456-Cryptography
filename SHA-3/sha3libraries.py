import hashlib #this is a built in package in python for hashing
from PyPDF2 import PdfReader, PdfWriter #package to work with pdfs
from Crypto.Hash import KangarooTwelve #package to get kangaroo twelve

data = input("Input some data to hash: ")
print('\nHASHLIB-SHA3: data = ' + data + '\n')
#has all sha3 variations
m224 = hashlib.sha3_224()
m256 = hashlib.sha3_256()
m384 = hashlib.sha3_384()
m512 = hashlib.sha3_512()

#for text
m224.update(data.encode())
m256.update(data.encode())
m384.update(data.encode())
m512.update(data.encode())

#print out the digests
print('224: ' + m224.hexdigest())
print('256: ' + m256.hexdigest())
print('384: ' + m384.hexdigest())
print('512: ' + m512.hexdigest())

#use hashlib on files too
print('\nHASHLIB-SHA3: data as a file\n')

#function to corrupt the file, just adds a blank page to the end
def corrupt(file):
    out = PdfWriter()
    pdfOne = PdfReader(open(file, "rb"))
    pdfTwo = PdfReader(open("blank.pdf", "rb"))

    for i in range(len(pdfOne.pages)): #this loop adds all the pages in the file
        out.add_page(pdfOne.pages[i])

    out.add_page(pdfTwo.pages[0]) #this adds the extra page, 'corrupting the file'

    outputStream = open("sha3.pdf", "wb")
    out.write(outputStream)
    outputStream.close()

#for a file
with open('sha3.pdf', 'rb') as f:
    digest = hashlib.file_digest(f, "sha3_256")
print('256: ' + digest.hexdigest())

input('Press enter to \'corrupt\' the file and you will see the hash change')
corrupt('sha3.pdf')

with open('sha3.pdf', 'rb') as f:
    digest = hashlib.file_digest(f, "sha3_256")
print('256: ' + digest.hexdigest())

print('\nHASHLIB-SHAKE: data  = ' + data + '\n')

#also has all shake variations
n = hashlib.shake_256()

n.update(data.encode())
#different length outputs
print('32 byte (256 bit) output: ' + n.hexdigest(32))
print('43 byte (344 bit) output: ' + n.hexdigest(43))

K12 = KangarooTwelve.new(custom=b'stringforcustomization') #the custom is so that 2 hashes with different custom str but same data will have different digest
K12.update(b'Some data')
print('K12 w str1:', K12.read(26).hex()) #read takes how man bytes as output

K12 = KangarooTwelve.new(custom=b'otherstringfork12') #the custom is so that 2 hashes with different custom str but same data will have different digest
K12.update(b'Some data')
print('K12 w str2:', K12.read(26).hex()) #read takes how man bytes as output


'''
from Crypto.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512
h_obj = SHA3_224.new()
h_obj.update(b'hello world')
print('SHA3_224:', h_obj.hexdigest())

h_obj = SHA3_256.new()
h_obj.update(b'hello world')
print('SHA3_256:',h_obj.hexdigest())


NOTE Below is all for Crypto.Hash
.new() can take a data= argument for data

hash_object.update(b'Second')
hash_object.update(b'Third')
The two steps above are equivalent to:
hash_object.update(b'SecondThird')
'''
'''
#SHA-3 Family
from Crypto.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512
h_obj = SHA3_224.new()
h_obj.update(b'Some data')
print('SHA3_224:', h_obj.hexdigest())

h_obj = SHA3_256.new()
h_obj.update(b'Some data')
print('SHA3_245:',h_obj.hexdigest())

h_obj = SHA3_384.new()
h_obj.update(b'Some data')
print('SHA3_384:',h_obj.hexdigest())

h_obj = SHA3_512.new()
h_obj.update(b'Some data')
print('SHA3_512:',h_obj.hexdigest())

#XOF(extendable output function) Shake/cShake
from Crypto.Hash import SHAKE128, SHAKE256, KangarooTwelve

shake = SHAKE128.new()
shake.update(b'Some data')
print('SHAKE128:', shake.read(26).hex()) #read takes how man bytes as output

shake = SHAKE256.new()
shake.update(b'Some data')
print('SHAKE256:', shake.read(26).hex()) #read takes how man bytes as output

K12 = KangarooTwelve.new(custom=b'stringforcustomization') #the custom is so that 2 hashes with different custom str but same data will have different digest
K12.update(b'Some data')
print('K12 w str1:', K12.read(26).hex()) #read takes how man bytes as output

K12 = KangarooTwelve.new(custom=b'otherstringfork12') #the custom is so that 2 hashes with different custom str but same data will have different digest
K12.update(b'Some data')
print('K12 w str2:', K12.read(26).hex()) #read takes how man bytes as output

#there is also use in message passing
from Crypto.Hash import KMAC128, KMAC256 #128 has 16 byte key, 256 has 32 byte key

secret = b'Sixteen byte key'
mac = KMAC128.new(key=secret, mac_len=16) #mac_len is an extra parameter for output
mac.update(b'Hello')
print('KMAC128:', mac.hexdigest())

#cant figure out what else to do
'''