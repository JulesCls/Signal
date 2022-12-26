import random,json,os,secrets
from server import Server
from typing import Tuple,TypedDict,Dict,List
from utils import expo_rapide
from elgamal import Elgamal


class idCouple(TypedDict):
    public : int
    private : int

    

class User:
    _name:str = ""
    _id:idCouple #public/private id
    _server:Server = Server()
    _master_key = None
    _pre_keys_list:List[int]
    _sig_pk:idCouple
    _user_directory:str = None
    _current_target:str = None


    def __init__(self,_name:str) -> None:
        self._pre_keys_list = list()
        self._name = _name
        self._user_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),self._name))
        self._id = {"public": None, "private" : None}
        if not(self.load_saved_info()):
            self._id["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._id["public"] = expo_rapide(self._server.get_public_generator(),self._id["private"],self._server.get_public_prime())
            self._sig_pk = {"public": None, "private" : None}
            # self._sig_pk["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            # self._sig_pk["public"] = expo_rapide(self._server.get_public_generator(),self._sig_pk["private"],self._server.get_public_prime())
            self.write_info()
        self._pre_keys_list = self._load_pre_keys()

    def write_info(self): #write public/private couple into user_name/.priv file to load it later
        directory = self._user_directory
        if not(os.path.exists(directory)):
            os.mkdir(directory)
        directory+= "/.priv"
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps(self._id))
        directory = self._user_directory + "/.pub"  #write public key into user_name/.pub file to use it in next steos by servor
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps({"public_id" : self._id["public"]}))

    def load_saved_info(self) -> bool:
        directory = self._user_directory
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

    def get_name(self) -> str:
        return self._name

    
    def send_message(self,message:str,target:str) -> bool:
        self._server.send_message(self,message,target)

    def get_initialization_keys_x3dh(self) -> dict:
        elgamal = Elgamal()
        return {
            "ID": self._id["public"],
            # "SigPK": self._sig_pk["public"],
            # "Sig(SigPk;ID)" : elgamal.sign(str(self._sig_pk["public"]).encode(),self._id["private"]),
            "SigPK": self._id["public"], # need to change for daily change
            "Sig(SigPk;ID)" : elgamal.sign(str(self._id["public"]).encode(),self._id["private"]),
            "OtPK": [public for _,public in self.generate_pre_keys()]
        }

    def generate_sig(self):
        elgamal = Elgamal()
        self._pk_pub = secrets.randbelow(self._server.get_public_prime()-2)
        self._pk_secret = expo_rapide(self._server.get_public_generator(),self._pk_pub,self._server.get_public_prime())
        return [self._id["public"],self._pk_pub,elgamal.sign(self._pk_pub.to_bytes(256,"big"),self._id["private"])]



    def connect_to_server(self) -> bool:
        pass

    #connect to server
        #ask server if it has data 
        #send if not

    #connect to client je veux envoyer à truc
        #check si on a un fichier name.key
        #si oui récup données publiques target et calcul DH
        #si non a nous de récup les data si elles existentes sinon en attente


    def _load_pre_keys(self):
        directory = os.path.join(self._user_directory,"./otpk")
        if os.path.exists(directory):
            with open(directory,"r") as f:
                return json.loads(f.read())
        return {}


    def _save_pre_keys(self):
        directory = os.path.join(self._user_directory,"./otpk")
        with open(directory,"w") as f:
            f.write(json.dumps(self._pre_keys_list))

    def connect_to_conversation(self,target:str):
        self._current_target = target
        print(self._server.connect_user_to_target(self,target))


    def generate_pre_keys(self):
        new_pre_keys = []
        for _ in range(4):
            private_pre_key = secrets.randbelow(self._server.get_public_prime()-2)
            new_pre_keys.append((private_pre_key,expo_rapide(self._server.get_public_generator(),private_pre_key,self._server.get_public_prime())))
        self._pre_keys_list += new_pre_keys
        self._save_pre_keys()
        return new_pre_keys

if __name__ == "__main__":
    alice = User("Alice")
    data = alice.generate_sig()
    elgamal = Elgamal()
    print(elgamal.verify(data[1].to_bytes(256,"big"),*data[2],data[0]))
