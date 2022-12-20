import json
from typing import Tuple

class Server:
    _instance = None
    _public_prime = None
    _public_generator = None

    _public_info_storage = "1024bits.txt"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(cls)
        return cls._instance

    def get_public_prime_and_generator_as_dict(self): #return public p and g as dict
        if None in [self._public_generator,self._public_prime]:
            self.read_prime_generator_from_file()
        return {"prime_number":self._public_prime,"generator":self._public_generator}

    def get_public_prime_and_generator_as_tuple(self) -> Tuple[int,int]: #return public p and g as tuple
        if None in [self._public_generator,self._public_prime]:
            self.read_prime_generator_from_file()
        return (self._public_prime,self._public_generator)

    


    def read_prime_generator_from_file(self) -> None: #load prime number and generator from file
        with open(self._public_info_storage,"r") as f:
            data = json.loads(f.read())
            self._public_prime = data["prime_number"]
            self._public_generator = data["generator_element"]
        if None in [self._public_generator,self._public_prime]:
            raise Exception("Le nom de fichier contenant les nombres publics du démarrage sont incorrectes ou bien le format n'est pas respecté.")
            




if __name__ == "__main__":
    s1 = Server()
    s2 = Server()

    print(s1 == s2)
    p_g_as_dict = s1.get_public_prime_and_generator_as_dict()
    print(p_g_as_dict) # retrieve public P
    p,g = s2.get_public_prime_and_generator_as_tuple()
    print(f"Prime number: {p}")
    print(f"Generator element: {g}")
