import id_bezout
import lsfr

def chiffrementAffine(x,p,key):
    if x > p:
        raise Exception("Chiffrement affine : x > p")
    if len(key)!=2:
        raise Exception(f"Chiffrement affine : incorrect key {key} ")
    return (x*key[0] + key[1]) % p

def dechiffrementAffine(x,p,key):
    return ((x - key[1])*key[0]) % p

def xor(block,key):
    # print(bin(block),bin(key))
    # print('xor function :', bin(block^key))
    return block^key

def feistel(block,iterations,key,nextKeyGeneratorFunction,encryptionFunction,blockSize = 16,decryptionMode = False):
    keys = [key]
    for i in range (1,iterations):
        keys.append(nextKeyGeneratorFunction(keys[i-1]))
    size = blockSize//2
    g = block >> size
    mask = int('0'*size+'1'*size,2)
    d = block & mask
    print(keys)
    print(bin(g),bin(d))
    for i in range (0 ,iterations):
        if decryptionMode:
            d,g = g,d^encryptionFunction(keys[len(keys)-1-i],g)
        else:
            g,d = d,g^encryptionFunction(keys[i],d)
        

        print(bin(g),bin(d))
    return (g << size) + d

if __name__ =="__main__":
    m = 10
    key = (11,3)
    p=26
    c = chiffrementAffine(m,p,key)
    key_inv = (id_bezout.invWithBezout(key[0],26),key[1])
    m = dechiffrementAffine(c,p,key_inv)

    key = int('01001011',2)
    message = int('1001001101011010',2)
    iterations = 12
    c = feistel(message,iterations,key,lsfr.basicLsfr8bits,xor)
    
    reversed = feistel(c,iterations,key,lsfr.basicLsfr8bits,xor,decryptionMode=True)
    print("RESULTS")
    print(bin(c))
    print(reversed)
    print(message)
    