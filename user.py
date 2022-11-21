import primalNumber,random

class User:
    name = ""
    publicKey = None
    privateKey = None

    def __init__(self,name) -> None:
        self.name = name

        p = primalNumber.getPrimeNumber()
        generatorElement = random.randrange(1,p)
        self.privateKey =primalNumber.getPrimeNumber()
        self.publicKey = pow(generatorElement,self.privateKey)
    
    def getPublicKey(self):
        return self.publicKey
    
    def getPrivateKey(self):
        return self.privateKey
