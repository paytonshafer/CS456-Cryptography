#python3 code for sha3 cryptographic algorithm on strings less than 1600 bits
import numpy as np

#these are the 4 versions of sha3 w their respective weights and capacities
versions = {
    '224':{
        'l':224,
        'r':1152,
        'c':448
    },
    '256':{
        'l':256,
        'r':1088,
        'c':512
    },
    '384':{
        'l':384,
        'r':832,
        'c': 768
    },
    '512':{
        'l':512,   
        'r': 576,
        'c': 1024
    }
}

rho_matrix = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
iota_table = ['0000000000000000000000000000000000000000000000000000000000000001' , '0000000000000000000000000000000000000000000000001000000010000010' , '1000000000000000000000000000000000000000000000001000000010001010' , '1000000000000000000000000000000010000000000000001000000000000000' , '0000000000000000000000000000000000000000000000001000000010001011' , '0000000000000000000000000000000010000000000000000000000000000001' , '1000000000000000000000000000000010000000000000001000000010000001' , '1000000000000000000000000000000000000000000000001000000000001001' , '0000000000000000000000000000000000000000000000000000000010001010' , '0000000000000000000000000000000000000000000000000000000010001000' , '0000000000000000000000000000000010000000000000001000000000001001' , '0000000000000000000000000000000010000000000000000000000000001010', '0000000000000000000000000000000010000000000000001000000010001011' , '1000000000000000000000000000000000000000000000000000000010001011',  '1000000000000000000000000000000000000000000000001000000010001001', '1000000000000000000000000000000000000000000000001000000000000011', '1000000000000000000000000000000000000000000000001000000000000010', '1000000000000000000000000000000000000000000000000000000010000000', '0000000000000000000000000000000000000000000000001000000000001010', '1000000000000000000000000000000010000000000000000000000000001010', '1000000000000000000000000000000010000000000000001000000010000001', '1000000000000000000000000000000000000000000000001000000010000000', '0000000000000000000000000000000010000000000000000000000000000001', '1000000000000000000000000000000010000000000000001000000000001000']

#function to take binary to string
def binary_to_string(s, encoding='UTF-8'):
    byte_string = ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
    return byte_string.decode(encoding)

#function to take binary to hex
def binary_to_hex(bits):
    strbits = ''.join([str(x) for x in bits])
    hex = '%0*X' % ((len(strbits) + 3) // 4, int(str(strbits), 2))
    return hex.lower()

#pads A to be amultiple of r, A is an string of bits and r is the rate
#mine is different than actual sha-3 because of padding
def padding(A, r):
    remainder = len(A) % r
    new_len = ((len(A) // r) + 1) * r

    val = list('0' * new_len)
    val[new_len-8] = '1'

    if remainder == 0:
        return A
    else:
        out = A + '1' + ''.join(str(x) for x in (np.zeros(r - remainder - 2 ,dtype= int))) + '1'
        return out[:new_len]

# 1600 bits(1 dimensional array) to 3 dimensional array of 5x5x64
def _1Dto3D(A):
    A_out = np.zeros((5, 5, 64), dtype = int) # Initialize empty 5x5x64 array
    for i in range(5):
        for j in range(5):
            for k in range(64):
                if 64*(5*j + i) + k <= len(A)-1:
                    A_out[i][j][k] = A[64*(5*j + i) + k]
    return A_out

#3 dimensional array of 5x5x64 to 1600 bits(1 dimensional array)  
def _3Dto1D(A):
    A_out = np.zeros(1600, dtype = int) # Initialize empty array of size 1600
    for i in range(5):
        for j in range(5):
            for k in range(64):
                A_out[64*(5*j+i)+k] = A[i][j][k]
    return A_out

'''
These are the equations for the theta function, view the data as a 5x5 array of 64 len words 
C[x] = A[x,0]⊕A[x,1]⊕A[x,2]⊕A[x,3]⊕A[x,4] , x = 0,1,2,3,4 
D[x] = C[x-1]⊕rot(C[x+1],1) , x = 0,1,2,3,4 
A[x,y] = A[x,y]⊕D[x] , x,y = 0,1,2,3,4
'''
def theta(A):
    out = A 
    #the below generates our C array
    C = np.zeros((5, 64), dtype=int)
    for x in range(5):
        C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]

    D = np.zeros((5, 64), dtype=int)
    for x in range(5):
        D[x] = C[(x-1)%5] ^ np.append(C[(x+1)%5][1:],[C[(x+1)%5][0]])

    for x in range(5):
        for y in range(5):
            out[x][y] = A[x][y] ^ D[x]

    return out        

#B[y,2x+3y] = rot(A[x,y],r[x,y]), where r is the rho matrix
def rho_pi(A):
    out = np.zeros((5,5,64), dtype = int) # Initialize empty 5x5x64 array

    for x in range(5):
        for y in range(5):
            #l = l[3:] + l[:3] this is how you rotate left 3 positions
            out[y, (2*x + 3*y)%5] = np.append(A[x][y][rho_matrix[x][y]:], A[x][y][:rho_matrix[x][y]])

    return out

# A_out[i][j][k] = B[i][j][k] XOR ( (B^-1[i + 1][j][k] XOR 1) AND (B[i + 2][j][k]) )
def chi(B):
    out = np.zeros((5,5,64), dtype = int) # Initialize empty 5x5x64 array

    for i in range(5):
        for j in range(5):
            for k in range(64):
                out[i][j][k] = (B[i][j][k] + (((B[(i + 1)%5][j][k] + 1 )% 2) * (B[(i + 2)%5][j][k]))) % 2

    return out

#adding a constant to A[0][0]: A[0][0] = A[0][0] XOR RC[round-#]
def iota(A, round):
    RC = iota_table[round]

    for i in range(64):
        A[0][0][i] = (A[0][0][i] + int(RC[i])) % 2

    return A

#data is in a 3D array already
def sha3_f(data, rounds):
    out = data

    for i in range(rounds):
        A = theta(out)
        B = rho_pi(A)
        C = chi(B)
        out = iota(C, i)

    return out


def sha3(data, b, rounds, version): #this is where we will run the sha-3 algo
    absorbing = np.zeros(1600, dtype = int) # Initialize empty array of size 1600
    data_list = []

    r = version['r']

    #split data in r size blocks
    for i in range(len(data) // r):
        data_list.append(data[r*i:r*(i+1)])

    #absorbing phase
    for j in range(len(data_list)):
        for i in range(r):
            absorbing[i] = (absorbing[i] + int(data_list[j][i])) % 2

        absorbing = _1Dto3D(absorbing)

        f_out = sha3_f(absorbing, rounds)

        absorbing = _3Dto1D(f_out)

    #squeezing phase
    squeezing = _1Dto3D(absorbing)
    f_out = sha3_f(squeezing, rounds)
    squeezing = _3Dto1D(f_out)

    return binary_to_hex(squeezing[:version['l']])


if __name__=='__main__':
    #print('l elem_of {0, 1, 2, 3, 4, 5, 6}')
    l = 6#int(input('Please input your l to determine the state size(l=6 for sha-3): ')) # value of l = {0, 1, 2, 3, 4, 5, 6}
    b = 25*(2**l)  # b = state size (value of b = {25, 50, 100, 200, 400, 800, 1600} )
    rounds = 12 + 2*l #how many rounds in the f function
    output_len = versions[input('Please eneter the version of SHA3 (224, 256, 384, 512): ')]
    data = input('Please enter the data you\'d like to hash: ')
    #print('Running SHA-3 with state size of ' + str(b) + ' for ' + str(rounds) + ' rounds')
    
    bits = ''.join(format(ord(i), '08b') for i in data) #turn the message into bits
    padded = padding(bits, output_len['r']) #padd the messege

    hex_digest = sha3(padded, b, rounds, output_len) #send padded bits, state size, rounds, and version
    print(hex_digest)


