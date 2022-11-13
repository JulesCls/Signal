def lsfr(positions, size,value):
    mask = 0b111111
    if(max(positions)>size-1): return -1
    strValue = str(bin(value)[2:]).zfill(size)
    finalBit = None
    for position in positions:
        if finalBit == None :
            finalBit = bool(int(strValue[position]))
        else:
            finalBit = bool(finalBit) != bool(int(strValue[position]))
    value = value << 1
    if(finalBit): value+=1
    return value & mask
        

if __name__ == "__main__":
    positions = [2,4,5]
    size = 6
    value = 11
    value = lsfr(positions,size,value)
    print(value)
    value = lsfr(positions,size,value)
    print(value)
    value = lsfr(positions,size,value)
    print(value)
    value = lsfr(positions,size,value)
    print(value)
    value = lsfr(positions,size,value)
    print(value)
    value = lsfr(positions,size,value)
    print(value)
    value = lsfr(positions,size,value)
    print(value)
    