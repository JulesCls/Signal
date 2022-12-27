import random,json,os,secrets
from server import Server
from typing import Tuple,TypedDict,Dict,List
from utils import expo_rapide, concatenateSK
from elgamal import Elgamal
from HMAC256 import HMAC256
from message import sk_data




class idCouple(TypedDict):
    public : int
    private : int



class User:
    _name:str = ""
    _id:idCouple #public/private id
    _server:Server = Server()
    _sk = None
    _otpk_list:List[int]
    _pk:idCouple
    _user_directory:str = None
    _current_target:str = None



    def __init__(self,_name:str) -> None:
        self._otpk_list = list()
        self._name = _name
        self._user_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),self._name))
        self._id = {"public": None, "private" : None}
        if not(self.load_saved_info()):
            self._id["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._id["public"] = expo_rapide(self._server.get_public_generator(),self._id["private"],self._server.get_public_prime())
            self._pk = {"public": None, "private" : None}
            self._pk["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._pk["public"] = expo_rapide(self._server.get_public_generator(),self._pk["private"],self._server.get_public_prime())
            self.write_info()
        self._otpk_list = self._load_pre_otpk()
        if self._otpk_list is None or self._otpk_list == []:
            self.generate_otpk()


    def write_info(self): #write public/private couple into user_name/.priv file to load it later
        directory = self._user_directory
        if not(os.path.exists(directory)):
            os.mkdir(directory)
        directory+= f"/{self._name}.json"
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps({"id":self._id,"pk":self._pk}))
        # directory = self._user_directory + "/.pub"  #write public key into user_name/.pub file to use it in next steos by servor
        # if not(os.path.exists(directory)):
        #     with open(directory,"w") as f:
        #         f.write(json.dumps({"public_id" : self._id["public"]}))

    def load_saved_info(self) -> bool:
        directory = self._user_directory
        if not(os.path.exists(directory)):
            return False
        directory+= f"/{self._name}.json"
        if not(os.path.exists(directory)):
            return False
        with open(directory,"r") as f:
            data = json.loads(f.read())
            self._id = data["id"]
            self._pk = data["pk"]
        return True

    def get_public_id(self)-> int:
        return self._id["public"]

    def get_name(self) -> str:
        return self._name


    def connect_to_server(self):
        self._server.connect_user(self)


    def share_info_to_server(self):
        elgamal = Elgamal()
        return {
            "id": self._id["public"],
            "pk": self._pk["public"],
            "signature" : elgamal.sign(self._pk["public"].to_bytes(256,"big"),self._id["private"]),
            "otpk": [public for _,public in self._otpk_list]
        }
    
    def send_message(self,message:str,target:str) -> bool:
        if self._sk == None:
            sk_pub_data:sk_data = self._initialize_sk(target)
            self._server.send_message(self,message,target,sk_pub_data)
        else:
            self._server.send_message(self,message,target)

    def _initialize_sk(self,target) -> sk_data:

        kdf = HMAC256()
        target_data = self._server.share_public_info_target_to_user(target)
        ephemeral_key_private = secrets.randbelow(self._server.get_public_prime()-2)
        ephemeral_key_public = expo_rapide(self._server.get_public_generator(),self._id["private"],self._server.get_public_prime())
        dh1 = self._dh(self._id["private"],target_data["pk"])
        dh2 = self._dh(ephemeral_key_private,target_data["id"])
        dh3 = self._dh(ephemeral_key_private,target_data["pk"])
        dh4 = self._dh(ephemeral_key_private,target_data["otpk"])
        self._message_key = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x01')
        self._chain_key = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x02')
        return {"otpk":target_data["otpk"],"ephemeral":ephemeral_key_public}

    def get_pending_messages(self):
        self._server.get_message(self)
        
        

    
    def share_sk_pub_data(self,eph_pub,otpk_pub,target):
        pass

    def _dh(self,x1:int,x2:int):
        return expo_rapide(x2,x1,self._server.get_public_prime())


    #genereate signed pre-key
    def generate_sig(self):
        elgamal = Elgamal()
        self._pk_pub = secrets.randbelow(self._server.get_public_prime()-2)
        self._pk_secret = expo_rapide(self._server.get_public_generator(),self._pk_pub,self._server.get_public_prime())
        return [self._id["public"],self._pk_pub,elgamal.sign(self._pk_pub.to_bytes(256,"big"),self._id["private"])]

    #generate 4 one-time pre-keys 
    def generate_otpk(self):
        new_pre_keys = []
        for _ in range(10):
            private_pre_key = secrets.randbelow(self._server.get_public_prime()-2)
            new_pre_keys.append((private_pre_key,expo_rapide(self._server.get_public_generator(),private_pre_key,self._server.get_public_prime())))
        self._otpk_list += new_pre_keys
        self._save_otpk()
        return new_pre_keys

    
    def _load_pre_otpk(self):
        directory = os.path.join(self._user_directory,"./otpk.json")
        if os.path.exists(directory):
            with open(directory,"r") as f:
                return json.loads(f.read())
        return self.generate_otpk()


    def _save_otpk(self):
        directory = os.path.join(self._user_directory,"./otpk.json")
        with open(directory,"w") as f:
            f.write(json.dumps(self._otpk_list))
    #connect to server
        #ask server if it has data 
        #send if not

    #connect to client je veux envoyer à truc
        #check si on a un fichier name.key
        #si oui récup données publiques target et calcul DH
        #si non a nous de récup les data si elles existentes sinon en attente


    

if __name__ == "__main__":
    alice = User("Alice")
    # data = alice.generate_sig()
    # elgamal = Elgamal()
    # print(elgamal.verify(data[1].to_bytes(256,"big"),*data[2],data[0]))
