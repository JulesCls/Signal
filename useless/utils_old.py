import secrets,sys

def addIterationToDictionary(number,dictionary):
    if(number in dictionary):
        dictionary[number] +=1
    else:
        dictionary[number] = 1

def generateRandomSplitInt(numberSize, sectionNumber):
    value = secrets.randbits(numberSize)
    splitNumber = []
    sectionSize = numberSize//sectionNumber
    if numberSize % sectionNumber != 0:
        return "Cannot split because of unequal sections"
    else:
        mask = (1 << sectionSize) - 1
        for i in range(sectionNumber):
            splitNumber.append(value & mask)
            value >>= sectionSize
        splitNumber.reverse()
        return splitNumber

def groupByBlock(blockSize, input):     #split a string into a list of blocks with a certain size of bits
    blocks = []
    if isinstance(input,int):
        blocks = groupByBits(6,input)
        return blocks
    else:
        for i in range(0,len(input),blockSize//8):
            blocks.append(input[i:(i+blockSize//8)])
        return blocks

def groupByBits(sizeList,input):            #return a sized list of binary numbers of integer input
    bits = []
    if isinstance(input,int) == False:
        return 'Need int input'
    else:
        for i in bin(input):
            bits.append(i)
        bits = bits[2:]
        while len(bits) < sizeList:
            bits.insert(0,0)
        for i in range(0,len(bits)):
            bits[i] = int(bits[i])
        return bits

def mergeBinaryString(block):    #convert a string block in its unicode integer   
    value = ord(block[0])
    for i in range(1,len(block)):
        value <<= 8
        value += ord(block[i])
    return value


def unMergeBinaryString(data):   #convert an integer into utf-8 encoded string
    mask = int("1"*8,2)
    res = ''
    while data > mask:
        value = data & mask
        res += chr(value)
        data >>= 8
    value = data & mask
    res += chr(value)
    res = res[::-1]
    return res

def concatenateList(bits):          #convert binary list into one integer
    for i in range(0,len(bits)):
        bits[i] = str(bits[i])
    string = ''.join(bits)       
    n = int(string, 2)
    return n

def stringToByteArray(string): #convert string to byte array
    res = bytearray(string, 'utf-16-be')
    return res

def bytesArrayToInt(bytesArray): #convert byte array to an integer
    res = 0
    for byte in bytesArray:
        res+= int(byte)
        res<<= 8
    res>>=8
    return res

def stringToInt(string): #convert string to integer
    return bytesArrayToInt(stringToByteArray(string))

def string_to_blocks(string: str):
    # Convert the string to a bytes object
    data = string.encode()
        
    # Initialize an empty list to store the blocks
    blocks = []
        
    # Split the data into blocks of 128 bits (16 bytes)
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        # If the block is not 64 bits long, pad it with 0s
        block = block.ljust(16, b'\x00')
        blocks.append(block)
            
    return blocks

def convert_int_list_to_utf8(int_list):
    # Convert the list of integers into a binary string
    binary = ''.join(str(i) for i in int_list)
    print(binary)
    # Convert the binary string into an integer
    integer = int(binary, 2)
    print(bin(integer))
    # Convert the integer into a bytes object of 64 bits
    b = integer.to_bytes(8, sys.byteorder)
    print(b)
    # Encode the bytes object as UTF-8
    utf8 = b.decode()
    return utf8

def rabin_miller(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = expo_rapide(a,s,n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = expo_rapide(x,2,n)
            if x == n - 1:
                break
        else:
            return False
    return True