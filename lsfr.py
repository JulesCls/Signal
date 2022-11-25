class LSFR:
    seed = None
    size = 0
    positions = []

    def __init__(self,seed,positions,size) -> None:
        if(max(positions)>size-1):
            raise Exception("LSFR Constructor : positons can not be greater than size")
        self.seed = seed
        self.positions = positions
        self.size = size

    def setSeed(self,seed):
        self.seed = seed

    def iterate(self):
        newBit = None
        for position in self.positions:
            tempValue = 1 & (self.seed >> position)
            if newBit==None:
                newBit = tempValue
            else:
                newBit=newBit&tempValue
        self.seed = (self.seed << 1) + newBit
        self.seed &= int("1"*self.size,2)
        return self.seed

    def reversedIteration(self):
        newBit = None
        for position in self.positions:
            tempValue = 1 & (self.seed >> position)
            if newBit==None:
                newBit = tempValue
            else:
                newBit=newBit&tempValue
        if(newBit == 1 ):
            self.seed+= pow(2,self.size)
        self.seed >>= 1
        return self.seed

    def getValue(self):
        return self.seed

class GeffeLSFR:
    LSFR1 = LSFR(int("0",2),[3,7,13],21)
    LSFR2 = LSFR(int("0",2),[0,8,11,20],21)
    LSFR3 = LSFR(int("0",2),[2,10,11,13,18,20],21)

    def __init__(self,seed) -> None:
        mask = int("1"*21,2)
        self.LSFR1.setSeed(seed&mask)
        self.LSFR2.setSeed((seed>>21)&mask)
        self.LSFR3.setSeed((seed>>42)&mask)
    
    def iterate(self):
        self.LSFR1.iterate()
        self.LSFR2.iterate()
        self.LSFR3.iterate()
        return self.getValue()

    def getValue(self):
        mask = 1
        x1 = self.LSFR1.getValue() & mask
        x2 = self.LSFR2.getValue() & mask
        x3 = self.LSFR3.getValue() & mask
        x2inv = 0
        if x2 != 0 : x2inv = 1
        y = (x1^x2) & (x2inv^x3)
        result = (((self.LSFR1.getValue() << 21) + self.LSFR2.getValue()) << 21) + self.LSFR3.getValue()
        result = result << 1 + y
        return result


def basicLsfr8bits(value):
    positions = [2,4,5]
    size = 8
    lsfr = LSFR(value,positions,size)
    return lsfr.iterate()


        

if __name__ == "__main__":
    # positions = [2,4,5]
    # size = 8
    # v =  int('01001011',2)
    # value = int('01001011',2)
    # print(value)
    # value = basicLsfr8bits(value)
    # print(value)
    # value = basicLsfr8bits(value)
    # print(value)
    # value = basicLsfr8bits(value)
    # print(value)
    geffe = GeffeLSFR(int("0011101100111111110011010001110001101111110000111010101000110111",2))
    print(geffe.iterate())
    print(geffe.iterate())
    #need to test geffe


    