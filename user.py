import primalNumber,random,json,os,secrets
from server import Server
from typing import Tuple,TypedDict
from expo_Rapide import mod_pow

class idCouple(TypedDict):
    public : int
    private : int

class User:
    name:str = ""
    id:idCouple #public/private id
    server:Server = Server()


    def __init__(self,name:str) -> None:
        self.name = name
        self.id = {"public": None, "private" : None}
        if not(self.load_saved_info()):
            self.id["public"] = secrets.randbelow(self.server.get_public_prime())
            self.write_public_info()
        self.id["private"] = mod_pow(self.server.get_public_generator(),self.id["public"],self.server.get_public_prime())

    def write_public_info(self):
        directory = self.name.lower()
        if not(os.path.exists(directory)):
            os.mkdir(directory)
        directory+= "/.pub"
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps({"public_id" : self.id["public"]}))

    def load_saved_info(self) -> bool:
        directory = self.name.lower()
        if not(os.path.exists(directory)):
            return False
        directory+= "/.pub"
        if not(os.path.exists(directory)):
            return False
        with open(directory,"r") as f:
            data = json.loads(f.read())
            self.id["public"] = data["public_id"]
        return True

    def get_public_id(self)-> int:
        return self.id["public"]

if __name__ == "__main__":
    alice = User("Alice")

    bob = User("Bobe")
    print(bob.get_public_id() == alice.get_public_id())
