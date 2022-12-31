import random,json,os,secrets
from server import Server
from typing import Tuple,TypedDict,Dict,List
from utils import expo_rapide, concatenateSK
from elgamal import Elgamal
from HMAC256 import HMAC256
from message import SK_DATA, Message
from RC4 import RC4
from pathlib import Path
from AES import AES




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
    _sks:Dict[str,SK]
    _pk:idCouple
    _user_directory:str = None



    def __init__(self,_name:str) -> None:
        self._name = _name
        self._user_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),self._name))
        self._id = {"public": None, "private" : None}
        if not(self.load_saved_info()):
            self._id["private"] = secrets.randbelow(self._server.get_public_prime()-2)
            self._id["public"] = expo_rapide(self._server.get_public_generator(),self._id["private"],self._server.get_public_prime())
            self.change_pk()
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

    def connect_to_target(self,target:str): #used to connect to target and fecth pending messages from the server
        self._sks = self._load_sk()
        self.get_pending_messages_from_target(target)
        self._server.connect_user(self)
    
    def disconnect_from_target(self): 
        self._save_sk()


    def share_info_to_server(self): #send public information stored privately to the server
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

    def change_pk(self):
        self._pk = {"public": None, "private" : None}
        self._pk["private"] = secrets.randbelow(self._server.get_public_prime()-2)
        self._pk["public"] = expo_rapide(self._server.get_public_generator(),self._pk["private"],self._server.get_public_prime())
        
    
    def send_message(self,msg:str,target:str, is_file:bool=False) -> bool: #send a message to a target
        self.get_pending_messages_from_target(target) #fetch if there is pending messages on the server, used to fetch sk
        self._random_sk_reinitialization(target) #try to reinitialize the secret key
        if is_file == False: #if simple message
            message =  Message(msg.encode(),self._name,target, None) #crate a message
            historic_message = Message(msg.encode(),self._name,target, None)
            if target not in self._sks.values(): #if no secret key shared with the targeted user
                    self._initalize_target_sk(target) #sk initialization
                    if self._sks[target] is None or None in self._sks[target].values():
                        sk_pub_data:SK_DATA = self._initialize_sk(target) #sk calculation for initialization
                        message.set_sk_data(sk_pub_data) #add sk data to the message
            self._add_messages(historic_message,sender=True) #add the message to the private storage of the user
            rc4 = RC4(self._sks[target]["message_key"]) 
            message.set_message(rc4.encrypt(message.get_message()))#encrypt the message with the secret key
            self._server.send_message(message) #send the message to the server for storage
            self._ratchet_sk(target) #ratchet the secret key for further use
        elif is_file == True: #same for file with further check
            filepath = msg
            if os.path.exists(filepath) == False:
                raise Exception("Le fichier n'existe pas, veuillez réessayer.")
            f = open(filepath,'rb')
            data_file = f.read()
            f.close()
            message =  Message(data_file,self._name,target, filepath)
            historic_message = Message(data_file,self._name,target, filepath)
            if target not in self._sks.values():
                    self._initalize_target_sk(target)
                    if self._sks[target] is None or None in self._sks[target].values():
                        sk_pub_data:SK_DATA = self._initialize_sk(target)
                        message.set_sk_data(sk_pub_data)
            self._add_messages(historic_message,sender=True)
            aes = AES()
            message.set_message(aes.encryption(message.get_message(),int.from_bytes(self._sks[target]["message_key"],'big'),'CBC'))
            self._server.send_message(message)
            self._ratchet_sk(target)
            

    def get_pending_messages_from_target(self,target:str): #fecth messages from server
        messages = self._server.get_user_messages_from_target(self,target)
        if messages != []:
            messages.sort(key= lambda x: x.get_timestamp()) #sort messages by timestamp
            for message in messages:
                if message.get_filepath() == None: #if it is not a file message
                    if message.get_sk_data(): #if a secret key has been generated by our sender we calculate the corresponding secret key
                        self._calculate_sk_from_received_data(message.get_sk_data(),message.get_sender()) 
                    rc4 = RC4(self._sks[message.get_sender()]["message_key"]) #decrypt the message with the secret key
                    clear_message = rc4.decrypt(message.get_message())
                    message.set_message(clear_message)
                    self._add_messages(message) #add the message to the private storage of the user
                    self._ratchet_sk(message.get_sender()) #ratche the secret key for further user
                if message.get_filepath() != None: #same than the previous if but with file and AES
                    if message.get_sk_data():
                        self._calculate_sk_from_received_data(message.get_sk_data(),message.get_sender())
                    aes = AES()
                    file_content = aes.decryption(message.get_message(),int.from_bytes(self._sks[message.get_sender()]["message_key"],'big'),'CBC')
                    self._ratchet_sk(message.get_sender())
                    if not(os.path.exists(os.path.join(self._user_directory,'files'))):
                        os.mkdir(os.path.join(self._user_directory,'files'))
                    file = open(os.path.join(self._user_directory,'files',os.path.basename(message.get_filepath())), "wb")
                    file.write(file_content)
                    file.close()
                    self._add_messages(message)
 
    def _random_sk_reinitialization(self,target): #used to randomly reset secret keys when sending messages
        x = random.randint(0,5)
        if x == 0:
            self._sks[target] = None

    def _initialize_sk(self,target) -> SK_DATA: #use to calculate a secret key when we do not have one already created with a user
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
        self._sks[target]["message_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x01')
        self._sks[target]["chain_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x02')
        return {"otpk":target_data["otpk"],"ephemeral":ephemeral_key_public,"signature":elgamal.sign(ephemeral_key_public.to_bytes(256,"big"),self._id["private"])}

    def _calculate_sk_from_received_data(self,received_data:SK_DATA,sender:str): #used to calculate a secret key when we found corresponding secret key creation on our sender message
        kdf = HMAC256()
        target_id = self._server.get_id_of_user(sender)
        elgamal = Elgamal()
        if not elgamal.verify(received_data["ephemeral"].to_bytes(256,"big"),*received_data["signature"],target_id): #signature verification
            raise Exception("Invalid ephemeral key signature verification.")
        #DH calculations
        dh1 = self._dh(self._pk["private"],target_id)
        dh2 = self._dh(self._id["private"],received_data["ephemeral"])
        dh3 = self._dh(self._pk["private"],received_data["ephemeral"])
        dh4 = self._dh(self._retrieve_otpk_private(received_data["otpk"]),received_data["ephemeral"])
        self._initalize_target_sk(sender)
        self._sks[sender]["message_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x01')
        self._sks[sender]["chain_key"] = kdf.digest(concatenateSK(dh1,dh2,dh3,dh4),b'\x02')

    def _ratchet_sk(self,target): #ratchet sk
        kdf = HMAC256()
        self._sks[target]["message_key"] = kdf.digest(self._sks[target]["chain_key"],b'\x01')
        self._sks[target]["chain_key"] = kdf.digest(self._sks[target]["chain_key"],b'\x02')
 

    def _dh(self,x1:int,x2:int): #used to calculate shared key
        return expo_rapide(x2,x1,self._server.get_public_prime())

    def _initalize_target_sk(self,target): #initalize a target secret key
        if target not in self._sks.keys() or self._sks[target] == None or  None in self._sks[target].values():
            self._sks[target] = {"message_key":None,"chain_key":None}

    #used to load and save secret keys from user file to persist it between sessions
    def _save_sk(self):
        file = os.path.join(self._user_directory,"sk.json")
        with open(file,"w") as f:
            print(json.dumps(self._sks))
            f.write(json.dumps(self._sks))

    def _load_sk(self):
        file = os.path.join(self._user_directory,"sk.json")
        if os.path.exists(file):
            with open(file,"r") as f:
                return json.load(f)
        return {}

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

    '''
    Fonctions utilisées pour ajouter les messages aux conversations privées de chaques utilisateurs
    Lorsque qu'un message est recu il est déchiffré et ajouté à un fichier au niveau du dossier de chaque utilisateur
    Cela permet de sauvegarder les messages des conversations de chaque utilisateur
    '''
    def print_target_conversation(self,target:str):
        self.get_pending_messages_from_target(target)
        messages = self._load_messages_from_target(target)
        if messages == []:
            print("Vous n'avez pas de messages.")
        else:
            print(f"Conversation entre vous même et {target}")
            for message in messages:
                if message.get_filepath():
                    print(f"[{message.get_timestamp()}] {message.get_sender()} a envoyé le fichier {os.path.basename(message.get_filepath())}")
                else:
                    print(f"[{message.get_timestamp()}] {message.get_sender()}: {message.get_message().decode()}")               

    def _add_messages(self,message:Message,sender=False):
        message.clear_for_write()
        target = message.get_sender()
        if sender:
            target = message.get_recipient()
        talks = self._load_messages_from_target(target)
        talks.append(message)
        file = os.path.join(self._user_directory,"talks", target + ".json")
        with open(file,"w") as f:
            f.write(json.dumps(talks))

    def _load_messages_from_target(self,target) -> List[Message]:
        messages:List[Message] = []
        directory = os.path.join(self._user_directory,"talks")
        if not os.path.exists(directory):
            os.makedirs(directory)
        file = os.path.join(directory, target + ".json")
        if os.path.exists(file):
            with open(file,"r") as f:
                data = json.loads(f.read())
                for message in data:
                    messages.append(Message.load_json(json.dumps(message)))
        return messages

    #getters
    def get_public_id(self)-> int:
        return self._id["public"]

    def get_name(self) -> str:
        return self._name   