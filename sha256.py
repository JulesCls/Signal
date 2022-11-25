import utils, lsfr

def Ch(e,f,g):
    return (e&f)^(~(e)&g)

def Maj(a,b,c):
    return (a&b)^(a&c)^(b&c)

class E0():
    rotate2 = lsfr.LSFR(0,[0],32)
    rotate13 = lsfr.LSFR(0,[0],32)
    rotate22 = lsfr.LSFR(0,[0],32)
    baseValue = 0
    
    def doRotations(self) -> None:
        self.rotate2.setSeed(self.baseValue)
        for _ in range(2):
            self.rotate2.reversedIteration()
        self.rotate13.setSeed(self.baseValue)
        for _ in range(13):
            self.rotate13.reversedIteration()
        self.rotate22.setSeed(self.baseValue)
        for _ in range(22):
            self.rotate22.reversedIteration()

    def operate(self,value) -> int:
        self.baseValue = value
        self.doRotations()
        return self.rotate2.getValue() ^ self.rotate13.getValue() ^ self.rotate22.getValue() 

class E1():
    rotate6 = lsfr.LSFR(0,[0],32)
    rotate11 = lsfr.LSFR(0,[0],32)
    rotate25 = lsfr.LSFR(0,[0],32)
    baseValue = 0
    
    def doRotations(self) -> None:
        self.rotate6.setSeed(self.baseValue)
        for _ in range(6):
            self.rotate6.reversedIteration()
        self.rotate11.setSeed(self.baseValue)
        for _ in range(11):
            self.rotate11.reversedIteration()
        self.rotate25.setSeed(self.baseValue)
        for _ in range(25):
            self.rotate25.reversedIteration()

    def operate(self,value) -> int:
        self.baseValue = value
        self.doRotations()
        return self.rotate6.getValue() ^ self.rotate11.getValue() ^ self.rotate25.getValue() 

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
    mod = pow(2,32)
    sigma0 = Sigma0()
    sigma1 = Sigma1()
    e1 = E1()
    e0 = E0()
    textInput = ""
    treatedBlock = None
    m = []
    w = []
    originalLength = 0
    H0 = 0x6a09e667
    H1 = 0xbb67ae85
    H2 = 0x3c6ef372
    H3 = 0xa54ff53a
    H4 = 0x510e527f
    H5 = 0x9b05688c
    H6 = 0x1f83d9ab
    H7 = 0x5be0cd19
    ROUND_CONSTANTS = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
)
    N = 1
    a = H0
    b = H1
    c = H2
    d = H3
    e = H4
    f = H5
    g = H6
    h = H6

        

    def hash(self,textInput) -> str:
        self.textInput = textInput
        self.preProcess()
        print(bin(self.textInput))
        for i in range(self.N):
            self.iterateThroughBlocks()
            self.calculateW()
            self.setVariables()
            self.calculateVariables()
            self.setHVariables()
        self.postProcess()
        
        return self.textInput

    def preProcess(self):
        self.originalLength = len(self.textInput)*8
        self.N = self.originalLength // 512
        if (self.originalLength > (self.N*512)-64):
            self.N+=1
        self.textInput = utils.mergeBinaryString(self.textInput)
        self.textInput <<= 1
        self.textInput+=1
        self.textInput <<= (512-(self.originalLength%512)-1)
        self.textInput+=self.originalLength

    def postProcess(self):
        self.textInput = "" + hex(self.H0)+hex(self.H1)+hex(self.H2)+hex(self.H3)+hex(self.H4)+hex(self.H5)+hex(self.H6)+hex(self.H7)

    def iterateThroughBlocks(self):
        input = self.textInput
        for _ in range(16):
            self.m.insert(0,input & (int("1"*32,2)))
            input = input>>32


    def calculateW(self):
        for i in range(len(self.m)):
            self.w.append(self.m[i])
        for t in range(16,64):
            wt = (self.sigma1.operate(self.w[t-2]) + self.w[t-7] + self.sigma0.operate(self.w[t-15]) + self.w[t-16]) % self.mod
            wt%=pow(2,32)
            self.w.append(wt)

    def calculateVariables(self):
        for t in range(64):
            T1 = (self.h + self.e1.operate(self.e) + Ch(self.e,self.f,self.g) + self.ROUND_CONSTANTS[t] + self.w[t]) % self.mod
            T2 = (self.e0.operate(self.a) + Maj(self.a,self.b,self.c)) % self.mod
            self.h = self.g
            self.g = self.f
            self.f = self.e
            self.e = (self.d + T1) % self.mod
            self.d = self.c
            self.c = self.b
            self.b = self.a
            self.a = (T1 + T2) % self.mod
            

    
    def setVariables(self):
        
        self.a = self.H0
        self.b = self.H1
        self.c = self.H2
        self.d = self.H3
        self.e = self.H4
        self.f = self.H5
        self.g = self.H6
        self.h = self.H7

    def setHVariables(self):
        self.H0 = (self.a + self.H0)%self.mod
        self.H1 = (self.b + self.H1)%self.mod
        self.H2 = (self.c + self.H2)%self.mod
        self.H3 = (self.d + self.H3)%self.mod
        self.H4 = (self.e + self.H4)%self.mod
        self.H5 = (self.f + self.H5)%self.mod
        self.H6 = (self.g + self.H6)%self.mod
        self.H7 = (self.h + self.H7)%self.mod



if __name__ == "__main__":
    sha = sha256()
    # print(bin(sha.getHash()))
    # s0 = sigma0()
    print(sha.hash("Yo"))
    # print(bin(s0.operate(int("11000111_00011100_01100100_11000001",2))))
    