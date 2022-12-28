import random,json,os,secrets
from server import Server
from typing import Tuple,TypedDict,Dict,List
from utils import expo_rapide, concatenateSK
from elgamal import Elgamal
from HMAC256 import HMAC256
from message import SK_DATA, Message
from RC4 import RC4




class idCouple(TypedDict):
    public : int
    private : int

class SK(TypedDict):
    chain_key:bytes
    message_key:bytes



class User:
    _name:str = ""
    _id:idCouple #public/private id
    _server:Server = Server()
    _sk:SK = None
    _pk:idCouple
    _user_directory:str = None



    def __init__(self,_name:str) -> None:
        self._name = _name
        self._sk =self._pk = {"chain_key": None, "message_key" : None}
        self._user_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),self._name))
        self._id = {"public": None, "private" : None}
        if not(self.load_saved_info()):
            self._id["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._id["public"] = expo_rapide(self._server.get_public_generator(),self._id["private"],self._server.get_public_prime())
            self._pk = {"public": None, "private" : None}
            self._pk["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._pk["public"] = expo_rapide(self._server.get_public_generator(),self._pk["private"],self._server.get_public_prime())
            self.write_info()


    def write_info(self): #write public/private couple into user_name/.json file to load it later
        directory = self._user_directory
        if not(os.path.exists(directory)):
            os.mkdir(directory)
        directory+= f"/{self._name}.json"
        if not(os.path.exists(directory)):
            with open(directory,"w") as f:
                f.write(json.dumps({"id":self._id,"pk":self._pk}))

    def load_saved_info(self) -> bool: #load info from user_name/.json file
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

    def connect_to_server(self):
        self._server.connect_user(self)


    def share_info_to_server(self):
        elgamal = Elgamal()
        otpk_list = self._load_otpk()
        if otpk_list == []:
            otpk_list = self.generate_otpk()
        return {
            "id": self._id["public"],
            "pk": self._pk["public"],
            "signature" : elgamal.sign(self._pk["public"].to_bytes(256,"big"),self._id["private"]),
            "otpk": [public for _,public in otpk_list]
        }
    
    def send_message(self,message:str,target:str) -> bool:
        message =  Message(message.encode(),self._name,target)
        if None in self._sk.values():
            sk_pub_data:SK_DATA = self._initialize_sk(target)
            message.set_sk_data(sk_pub_data)
        rc4 = RC4(self._sk["message_key"])
        message.set_message(rc4.encrypt(message.get_message()))
        self._server.send_message(message)
        self._ratchet_sk()

    def _initialize_sk(self,target) -> SK_DATA:
        kdf = HMAC256()
        elgamal = Elgamal()
        target_data = self._server.share_public_info_target_to_user(target)
        if not elgamal.verify(target_data["pk"].to_bytes(256,"big"),*target_data["signature"],target_data["id"]):
            raise Exception("Invalid pk signature verification")

        ephemeral_key_private = secrets.randbelow(self._server.get_public_prime()-2)
        ephemeral_key_public = expo_rapide(self._server.get_public_generator(),ephemeral_key_private,self._server.get_public_prime())
        dh1 = self._dh(self._id["private"],target_data["pk"])
        dh2 = self._dh(ephemeral_key_private,target_data["id"])
        dh3 = self._dh(ephemeral_key_private,target_data["pk"])
        dh4 = self._dh(ephemeral_key_private,target_data["otpk"])
        self._sk["message_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x01')
        self._sk["chain_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x02')
        return {"otpk":target_data["otpk"],"ephemeral":ephemeral_key_public,"signature":elgamal.sign(ephemeral_key_public.to_bytes(256,"big"),self._id["private"])}

    def _calculate_sk_from_received_data(self,received_data:SK_DATA,sender:str):
        kdf = HMAC256()
        target_id = self._server.get_id_of_user(sender)
        elgamal = Elgamal()
        if not elgamal.verify(received_data["ephemeral"].to_bytes(256,"big"),*received_data["signature"],target_id):
            raise Exception("Invalid ephemeral key signature verification.")
        dh1 = self._dh(self._pk["private"],target_id)
        dh2 = self._dh(self._id["private"],received_data["ephemeral"])
        dh3 = self._dh(self._pk["private"],received_data["ephemeral"])
        dh4 = self._dh(self._retrieve_otpk_private(received_data["otpk"]),received_data["ephemeral"])
        self._sk["message_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x01')
        self._sk["chain_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x02')


    def get_pending_messages(self): #fecth messages from server
        messages = self._server.get_user_messages(self)
        if messages != []:
            messages.sort(key= lambda x: x.get_timestamp())
            for message in messages:
                if message.get_sk_data():
                    self._calculate_sk_from_received_data(message.get_sk_data(),message.get_sender())
                rc4 = RC4(self._sk["message_key"])
                clear_message = rc4.decrypt(message.get_message())
                self._ratchet_sk()
                print(f"{message.get_sender():<10}{clear_message.decode()}")

        
    def _ratchet_sk(self): #ratchet sk
        kdf = HMAC256()
        if None not in self._sk.keys():
            self._sk["message_key"] = kdf.digest(self._sk["chain_key"],b'\x01')
            self._sk["chain_key"] = kdf.digest(self._sk["chain_key"],b'\x02')
            

    def _dh(self,x1:int,x2:int): #used to calculate shared key
        return expo_rapide(x2,x1,self._server.get_public_prime())

    #used to load and save otpk keys
    def _load_otpk(self) -> List[Tuple[int,int]]:
        directory = os.path.join(self._user_directory,"./otpk.json")
        if os.path.exists(directory):
            with open(directory,"r") as f:
                return json.loads(f.read())
        return []

    def _save_otpk(self,otpk_list:List[Tuple[int,int]]):
        directory = os.path.join(self._user_directory,"./otpk.json")
        with open(directory,"w") as f:
            f.write(json.dumps(otpk_list))

    def _retrieve_otpk_private(self,otpk_to_find:int):
        for otpk in self._load_otpk():
            private,public = otpk
            if public == otpk_to_find:
                self._remove_otpk((private,public))
                return private

    def _remove_otpk(self,otpk_tuple:Tuple[int,int]):
        otpk_list = self._load_otpk()
        for otpk in otpk_list:
            priv, pub = otpk
            if priv == otpk_tuple[0] and pub == otpk_tuple[1]:
                otpk_list.remove(otpk)
                break
        self._save_otpk(otpk_list)

    #generate 4 one-time pre-keys 
    def generate_otpk(self) -> List[Tuple[int,int]]:
        otpk_list = self._load_otpk()

        new_pre_keys = []
        for _ in range(20):
            private_pre_key = secrets.randbelow(self._server.get_public_prime()-2)
            new_pre_keys.append((private_pre_key,expo_rapide(self._server.get_public_generator(),private_pre_key,self._server.get_public_prime())))
        otpk_list+= new_pre_keys
        self._save_otpk(otpk_list)
        return otpk_list

    #getters
    def get_public_id(self)-> int:
        return self._id["public"]

    def get_name(self) -> str:
        return self._name   