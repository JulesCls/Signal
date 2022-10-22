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

if __name__ == "__main__":
    print(generateSplitInt(128,4))
    