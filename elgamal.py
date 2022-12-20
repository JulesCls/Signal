from server import Server
import sha256,expo_Rapide,secrets
from user import User


class Elgamal():
    SERVER = Server()
    p,g = SERVER.get_public_prime_and_generator_as_tuple()

    def keyGeneration(self):
        secretKey = secrets.randbelow(self.p-1) #user.getPrivateID()
        publicKey = expo_Rapide.mod_pow(self.g,secretKey,self.p) #user.getPublicID
        return (publicKey,secretKey)

    def signatureGen():
        

if __name__ == "__main__":
    elg = Elgamal()
    print(elg.keyGeneration())
    test = 'test'
    print(bytes(test))
