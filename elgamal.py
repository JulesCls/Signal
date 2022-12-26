from server import Server
import secrets
from user import User
from utils import expo_rapide


class Elgamal():
    SERVER = Server()
    p,g = SERVER.get_public_prime_and_generator_as_tuple()
    

if __name__ == "__main__":
    test = 'test'
    elg = Elgamal()
    print(elg.keyGeneration(test))
