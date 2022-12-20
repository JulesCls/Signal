import primalNumber, euclide, secrets, id_bezout,math
from utils import expo_rapide

class Rsa:
    size = None

    def __init__(self,size: int):
        self.size = size
    
    def generateKeys(self):
        p = primalNumber.getPrimeNumber(self.size)          #generate randomly the 2 first factors
        q = primalNumber.getPrimeNumber(self.size)
        n = p * q                                           #generate encrypt common module
        phi = (p-1)*(q-1)

        e = None
        while e == None:                                    #calculate public key which coprime with phi
            x = secrets.randbelow(phi)
            if euclide.pgcdEuclide(x,phi) == 1:
                e = x
        d = id_bezout.invWithBezout(e,phi)                  #calculate private key d which is the invert of e mod n
        return {'privKeys': (n,d), 'pubKeys': (n,e)}

    def encrypt(self,message,keyPair: dict):
        pub = keyPair['pubKeys']
        if type(message) == int:
            cypher = expo_rapide(message,pub[1],pub[0]) # C congrue M**e mod n
            return cypher
        else:
            raise Exception("Incorrect type of input : Need int to encrypt the message")
    
    def decrypt(self,cypher,keyPair: dict):
        priv = keyPair['privKeys']
        if type(cypher) == int:
            message = expo_rapide(cypher,priv[1],priv[0]) # M congrue C**d mod n
            return message
        else:
            raise Exception("Incorrect type of input : Need int to decrypt the message")

if __name__ == "__main__":

    message = secrets.randbits(512)
    print(message)
    rsa = Rsa(512)
    keyPair = rsa.generateKeys()
    print(keyPair)
    cypher = rsa.encrypt(message,keyPair)
    print(cypher)
    message = rsa.decrypt(cypher,keyPair)
    print(message)


