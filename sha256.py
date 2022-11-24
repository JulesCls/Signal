import utils, lsfr

class Sigma0:
    rotate7 = lsfr.LSFR(0,[0],32)
    rotate18 = lsfr.LSFR(0,[0],32)
    baseValue = 0
    
    def doRotations(self) -> None:
        self.rotate7.setSeed(self.baseValue)
        for _ in range(7):
            self.rotate7.reversedIteration()
        self.rotate18.setSeed(self.baseValue)
        for _ in range(18):
            self.rotate18.reversedIteration()
        self.baseValue >>= 3

    def operate(self,value) -> int:
        self.baseValue = value
        self.doRotations()
        return self.rotate18.getValue() ^ self.rotate7.getValue() ^ self.baseValue


class Sigma1:
    rotate17 = lsfr.LSFR(0,[0],32)
    rotate19 = lsfr.LSFR(0,[0],32)
    baseValue = 0
    
    def doRotations(self) -> None:
        self.rotate17.setSeed(self.baseValue)
        for _ in range(17):
            self.rotate17.reversedIteration()
        
        self.rotate19.setSeed(self.baseValue)
        for _ in range(19):
            self.rotate19.reversedIteration()
        self.baseValue >>= 10

    def operate(self,value) -> int:
        self.baseValue = value
        self.doRotations()
        return self.rotate19.getValue() ^ self.rotate17.getValue() ^ self.baseValue


class sha256():
    sigma0 = Sigma0()
    sigma1 = Sigma1()
    textInput = ""
    m = []
    w = []
    originalLength = 0
    H0 = int("0x6a09e667",0)
    H1 = int("0xbb67ae85",0)
    H2 = int("0x3c6ef372",0)
    H3 = int("0xa54ff53a",0)
    H4 = int("0x510e527f",0)
    H5 = int("0x9b05688c",0)
    H6 = int("0x1f83d9ab",0)
    H7 = int("0x5be0cd19",0)
    N = 1
    a = H0
    b = H1
    c = H2
    d = H3
    e = H4
    f = H5
    g = H6
    h = H6

    def __init__(self,textInput) -> None:
        self.textInput = textInput
        self.preProcess()
        self.calculateW()

    def preProcess(self):
        self.originalLength = len(self.textInput)*8
        self.N = self.originalLength // 512
        if (self.originalLength > (self.N*512)-64):
            self.N+=1
        self.textInput = utils.mergeBinaryString(self.textInput)
        self.textInput <<= 1
        self.textInput+=1
        self.textInput <<= (512-self.originalLength-1)
        self.textInput+=self.originalLength
        for i in range(16):
            self.m.insert(0,(self.textInput>>(i*32)) & (int("1"*32,2)))

    def getHash(self) -> str:
        return self.textInput

    def calculateW(self):
        for i in range(len(self.m)):
            self.w.append(self.m[i])
        for t in range(16,64):
            wt = self.sigma1.operate(self.w[t-2]) + self.w[t-7] + self.sigma0.operate(self.w[t-15]) + self.w[t-16]
            wt%=pow(2,32)
            self.w.append(wt)
            print(t,bin(wt))  


if __name__ == "__main__":
    sha = sha256("RedBlockBlue")
    # print(bin(sha.getHash()))
    # s0 = sigma0()
    print(-3%5)
    # print(bin(s0.operate(int("11000111_00011100_01100100_11000001",2))))
    