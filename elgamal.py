from server import Server
import secrets
from utils import expo_rapide, inverse
from sha256 import SHA256
import math

class Elgamal():
    _p,_g = Server().get_public_prime_and_generator_as_tuple()
    sha = SHA256()

    #réutilisation des cles privées et publics d'un user
    # def keyGeneration(self):
    #     secretKey = secrets.randbelow(self._p-1) #user.getPrivateID()
    #     publicKey = expo_rapide(self._g,secretKey,self._p) #user.getPublicID
    #     return (publicKey,secretKey)
    
    def sign(self,message:bytes,private_key:int):
        y = self._generate_y()
        s1 = expo_rapide(self._g,y,self._p)
        y_inv = inverse(y,self._p-1)
        s2 = ((self._hash_to_int(message) - private_key * s1) * y_inv) % (self._p -1)
        return (s1,s2)

    def verify(self,message:bytes,s1:int,s2:int,public_key:int)->bool:
        message_value = expo_rapide(self._g,self._hash_to_int(message),self._p)
        verify_value = (expo_rapide(public_key,s1,self._p) * expo_rapide(s1,s2,self._p)) % self._p
        # verify_value = (pow(public_key,r) * pow(r,s)) % self._p
        return message_value == verify_value

    def _generate_y(self)->int:
        y = secrets.randbelow(self._p-2)
        while y==2 or math.gcd(y,self._p-1) != 1:
            y = secrets.randbelow(self._p-2)
        return y

    def _hash_to_int(self,data:bytes)->int:
        return int.from_bytes(self.sha.digest(data),"big")
