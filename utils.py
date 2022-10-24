import secrets

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

def concatenateInteger(list):
    for i in range(0,4):
        list[i] = list[i] << (32*(len(list)-(i+1)))
    output = list[0] | list[1] | list[2] | list[3]
    return output




if __name__ == "__main__":
    print(generateRandomSplitInt(128,4))
    