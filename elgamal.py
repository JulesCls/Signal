from server import Server
import secrets
from user import User
from utils import expo_rapide


class Elgamal():
    SERVER = Server()
    p,g = SERVER.get_public_prime_and_generator_as_tuple()

    def keyGeneration(self):
        secretKey = secrets.randbelow(self.p-1) #user.getPrivateID()
        publicKey = expo_rapide(self.g,secretKey,self.p) #user.getPublicID
        return (publicKey,secretKey)

    def signatureGen():
        pass

if __name__ == "__main__":
    elg = Elgamal()
    print(elg.keyGeneration())
    test = 'test'
    print(bytes(test))
