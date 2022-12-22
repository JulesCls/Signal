import random,json,os,secrets
from server import Server
from typing import Tuple,TypedDict
from utils import expo_rapide


class idCouple(TypedDict):
    public : int
    private : int

class User:
    _name:str = ""
    _id:idCouple #public/private id
    _server:Server = Server()


    def __init__(self,_name:str) -> None:
        self._name = _name
        self._id = {"public": None, "private" : None}
        if not(self.load_saved_info()):
            self._id["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._id["public"] = expo_rapide(self._server.get_public_generator(),self._id["private"],self._server.get_public_prime())
            self.write_info()

    def write_info(self): #write public/private couple into user_name/.priv file to load it later
        directory = self._name.lower()
        if not(os.path.exists(directory)):
            os.mkdir(directory)
        directory+= "/.priv"
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps(self._id))
        directory = self._name.lower() + "/.pub"  #write public key into user_name/.pub file to use it in next steos by servor
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps({"public_id" : self._id["public"]}))

    def load_saved_info(self) -> bool:
        directory = self._name.lower()
        if not(os.path.exists(directory)):
            return False
        directory+= "/.priv"
        if not(os.path.exists(directory)):
            return False
        with open(directory,"r") as f:
            self._id = json.loads(f.read())
        return True

    def get_public_id(self)-> int:
        return self._id["public"]

if __name__ == "__main__":
    alice = User("Alice")

    bob = User("Bobe")
    print(bob.get_public_id() == alice.get_public_id())
    p,g = alice._server.get_public_prime_and_generator_as_tuple()
    print(expo_rapide(g,alice._id["private"],p) == alice._id["public"])
