import hashlib
from PyPDF2 import PdfReader, PdfWriter #package to work with pdfs

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

data = input("\nInput some different data to hash: ")
m512_2 = hashlib.sha3_512()
m512_2.update(data.encode())
print('512: ' + m512_2.hexdigest())

#use hashlib on files too
print('\nHASHLIB-SHA3: data as a file\n')

#for a file
with open('sha3.pdf', 'rb') as f:
    digest = hashlib.file_digest(f, "sha3_256")
print('256: ' + digest.hexdigest())

input('Press enter to \'corrupt\' the file and you will see the hash change')
#corrupt('sha3.pdf')

with open('sha3.pdf', 'rb') as f:
    digest = hashlib.file_digest(f, "sha3_256")
print('256: ' + digest.hexdigest())

#then go through my SHA3 function