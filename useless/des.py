import utils
import feisteil
import lsfr
import codecs

def permutation(type, block: bytes):
    if type == 1:
        permutationList = [58, 50, 42, 34, 26, 18, 10, 2,
                           60, 52, 44, 36, 28, 20, 12, 4,
                           62, 54, 46, 38, 30, 22, 14, 6,
                           64, 56, 48, 40, 32, 24, 16, 8,
                           57, 49, 41, 33, 25, 17, 9, 1,
                           59, 51, 43, 35, 27, 19, 11, 3,
                           61, 53, 45, 37, 29, 21, 13, 5,
                           63, 55, 47, 39, 31, 23, 15, 7]
        bits = []
        res = []
        if len(block) != 8:
            raise ValueError("Block must be 64 bits long")
        for b in block:
            bit = bin(b)[2:].zfill(8)
            bits.extend([int(x) for x in bit])
        for i in permutationList:
            res.append(bits[i-1])
        res = utils.convert_int_list_to_utf8(res)
        return res
    
    elif type == 2:
        bits = utils.groupByBits(32, block)
        res = [None] * 32
        permutationList = [16,7,20,21,29,12,28,17,
                           1,15,23,26,5,18,31,10,
                           2,8,24,14,32,27,3,9,
                           19,13,30,6,22,11,4,25]
        for i,j in zip(permutationList, range(0,len(bits))):
            res[j] = bits[i-1]
        return res
    elif type == 3:
        return res
    else:
        raise Exception("Need arg : type 1 for PI, type 2 for PF and type 3 for PI-1")

def dloppement(block):
    block = utils.groupByBits(32,block)
    res = [None] * 48
    index = [32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]
    for i,j in zip(index, range(0,len(res))):
         res[j] = block[i-1]
    return res

def sBoxes(bList):
    res = []
    sBoxesList = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
                  0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
                  4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
                  15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
                  [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
                  3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
                  0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
                  13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
                  [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
                  13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
                  13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
                  1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
                  [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
                  13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
                  10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
                  3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
                  [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
                  14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
                  4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
                  11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
                  [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
                  10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
                  9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
                  4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
                  [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
                  13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
                  1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
                  6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
                  [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
                  1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
                  7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
                  2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
    for i in bList:
        bits = utils.groupByBits(6,i)
        line = int((2**1)*bits[0]+(2**0)*bits[5])
        column = int((2**3)*bits[1]+(2**2)*bits[2]+(2**1)*bits[3]+(2**0)*bits[4])
        index = bList.index(i)
        res.append(sBoxesList[index][(15*line)+column])
    return res
            

def desEncryptionFunction(key, block):      #f function of DES
    mask = int("1"*6,2)
    d = dloppement(block)                   #start dloppment function
    d = utils.concatenateList(d)            #convert binary list into one number
    dPrime  = d ^ key                       #XOR result with the subkey
    b = []
    b.append(dPrime & mask)                 #split the 48-bits number into 8*6-bits number list
    while len(b) < 8:
        dPrime >>= 6
        b.append(dPrime & mask)
    b.reverse()
    c = []
    c = sBoxes(b)                           #apply sBoxes on b list to get 8*4-bits number list
    for i in range(0,len(c)):               #convert this list in binary and merge it into a 32-bits binary number
        print(c)
        c[i] = bin(c[i])[2:].zfill(4)
    c = ''.join(c)
    print(c)
    c = int(c,2)
    res = utils.concatenateList(permutation(2,c))
    return res
    
def TDesEncrypt(block,key):
    if block > (2^64)-1:
        raise Exception("Block size is too long")
    else:
        cypher = feisteil.feistel(block,16,key,lsfr.basicLsfr8bits(key),desEncryptionFunction(key,block),64)
        return cypher
    

if __name__ == "__main__":
    # blocks = utils.string_to_blocks("Hello, world!")
    # i=[]
    # for block in blocks:
    #     res = permutation(1,block)
    #     print(block)
    #     print(res)
    
    b = '0b10011111'
    i = int(b,2)
    i = i.to_bytes(8, 'big')
    print(i.decode('hex'))