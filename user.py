import primalNumber,random,json,os

class User:
    name = ""
    publicKey = None
    privateKey = None

    def __init__(self,name) -> None:
        self.name = name
        self.generateKeys()
        self.publishKeys()
    
    def generateKeys(self):
        p = primalNumber.getPrimeNumber(length=2048)
        print("Prime done")
        generatorElement = random.randrange(1,p)
        print("generator element done")
        self.privateKey =primalNumber.getPrimeNumber(length=2048)
        print("private key done")
        self.publicKey = pow(generatorElement,self.privateKey,p)
        print("public key done")

    def getPublicKey(self):
        return self.publicKey
    
    def getPrivateKey(self):
        return self.privateKey


    def publishKeys(self):
        data = {
            'ID' : self.publicKey
        }
        filename = self.name.lower() + "/keys.pub","w"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,"w") as f:
            f.write(json.dumps(data))

if __name__ == "__main__":
    alice = User("Alice")
