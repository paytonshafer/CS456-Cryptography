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

print('\nHASHLIB-SHAKE: data = ' + data + '\n')

#also has all shake variations
n = hashlib.shake_256()

n.update(data.encode())
#different length outputs
shake = input('Please enter the amount of bytes you would like: ')
print(shake + ' byte (' + str(int(shake)*8) +' bit) output: ' + n.hexdigest(int(shake)))
print('32 byte (256 bit) output: ' + n.hexdigest(32))
print('43 byte (344 bit) output: ' + n.hexdigest(43))

print('\nCRYPTO.HASH-K12: data = ' + data + '\n')
[key1, key2] = input('Please enter two different keys seperated by a space: ').split(' ')
length = int(input('Please enter the number of bytes of output you\'d like: '))

K12 = KangarooTwelve.new(custom=key1.encode()) #the custom is so that 2 hashes with different custom str but same data will have different digest
K12.update(data.encode())
print('K12 key = ' + key1 + ': ' +  K12.read(length).hex()) #read takes how man bytes as output

K12 = KangarooTwelve.new(custom=key2.encode()) #the custom is so that 2 hashes with different custom str but same data will have different digest
K12.update(data.encode())
print('K12 key = ' + key2 + ': ' + K12.read(length).hex()) #read takes how man bytes as output