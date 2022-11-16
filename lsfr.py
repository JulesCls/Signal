def lsfr(positions, size,value):
    if(max(positions)>size-1): return -1
    newBit = None
    for position in positions:
        tempValue = 1 & (value >> position)
        if newBit==None:
            newBit = tempValue
        else:
            newBit=newBit&tempValue
    value = (value << 1) + newBit
    value &= int("1"*size,2)
    return value

def basicLsfr8bits(value):
    positions = [2,4,5]
    size = 8
    return lsfr(positions,size,value)


if __name__ == "__main__":
    positions = [2,4,5]
    size = 6
    value = int('01001011',2)
    print(value)
    value = basicLsfr8bits(value)
    print(value)
    value = basicLsfr8bits(value)
    print(value)
    