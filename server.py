import json, utils, os
from typing import Tuple

class Server:
    _instance = None
    _public_prime = None
    _public_generator = None
    _numbers_in_cache = False
    _server_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"server"))


    _public_info_storage = "pub.txt"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(cls)
        return cls._instance

    def get_public_prime_and_generator_as_dict(self): #return public p and g as dict
        self.read_prime_generator_from_file()
        return {"prime_number":self._public_prime,"generator":self._public_generator}

    def get_public_prime_and_generator_as_tuple(self) -> Tuple[int,int]: #return public p and g as tuple
        self.read_prime_generator_from_file()
        return (self._public_prime,self._public_generator)

    def get_public_prime(self) -> int: #return public p and g as tuple
        self.read_prime_generator_from_file()
        return self._public_prime

    def get_public_generator(self) -> int: #return public p and g as tuple
        self.read_prime_generator_from_file()
        return self._public_generator

    def read_prime_generator_from_file(self) -> None: #load prime number and generator from file
        if self._numbers_in_cache:
            return
        self._numbers_in_cache = True
        with open(self._public_info_storage,"r") as f:
            data = json.loads(f.read())
            self._public_prime = data["prime_number"]
            self._public_generator = data["generator_element"]
        if None in [self._public_generator,self._public_prime]:
            raise Exception("Le nom de fichier contenant les nombres publics du démarrage sont incorrectes ou bien le format n'est pas respecté.")
        

    def generate_new_public_numbers(self):
        p_g = utils.get_number_with_generator_element()
        with open(self._public_info_storage,"w") as f:
            f.write(json.dumps(p_g))
        print("Generation done.")

    def send_message(self,user,message:str,target:str) -> None:
        conversation_directory = self.get_conversation_directory_name(user,target)
        if os.path.exists(conversation_directory):
            pass
        else:
            #need to init conversation with x3dh
            os.makedirs(os.path.join(self._server_directory_path, user.get_name() +"-"+ target))
            self.initialize_key_share(user,conversation_directory)

        #else use ratchet

    def get_conversation_directory_name(self,user,target:str) -> str:
        conversation_directory = self._server_directory_path
        username = user.get_name()
        if username > target:
            conversation_directory =  os.path.join(conversation_directory, target +"-"+ username)
        else:
            conversation_directory =  os.path.join(conversation_directory, username +"-"+ target)
        return conversation_directory

    def initialize_key_share(self,user,conversation_directory:str) -> None:
        with open(os.path.join(conversation_directory,user.get_name() + ".keys") ,"w") as f:
            f.write(json.dumps(user.get_initialization_keys_x3dh()))

            





    

