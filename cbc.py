import utils
import des

def CBC(blocks, initialVector, encryptionFunction, key):  #return the list of blocks encrypted with a specific encryption function and CBC method
    firstBlock = initialVector ^ blocks[0]
    firstblock = encryptionFunction(firstblock,key)
    res = []
    res.append(firstBlock)
    for i in blocks:
        res.append(encryptionFunction(blocks[i+1]^res[i],key))
    return res



