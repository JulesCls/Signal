import json, utils, os, random
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



    def check_public_info_of_user(self,username):
        file = os.path.join(self._server_directory_path,username+".pub")
        if os.path.exists(file):
            with open(file,"r") as f:
                    return json.loads(f.read())
        return None
        
    def publish_user_info(self,user):
        file = os.path.join(self._server_directory_path,user.get_name()+".pub")
        with open(file,"w") as f:
            f.write(json.dumps(user.share_info_to_server()))

    def update_user_info(self,user):
        data = self.check_public_info_of_user(user.get_name())
        if user.share_info_to_server() != data:
            self.publish_user_info(user)
        

    def connect_user(self,user):
        self.update_user_info(user)

   

    ##to rework


    def _conversation_exists(self,conversation_directory) -> bool:
        return os.path.exists(conversation_directory)
           

    def _check_for_pre_keys(self,conversation_directory,target) -> None|int:
        file = os.path.join(conversation_directory,target+".keys")
        target_info = None
        if os.path.exists(file):
            with open(file,"r") as f:
                target_info = json.loads(f.read())
                key_number = random.randint(0,len(target_info["OtPK"])-1)
                target_info["OtPK"] = target_info["OtPK"][key_number] 
                with open(os.path.join(conversation_directory,target+".key"),"w") as f2:
                    f2.write(str(key_number))
            os.remove(file)
            return target_info            
        return target_info

    def _check_for_selected_pre_key(self,conversation_directory,target) -> None|int:
        file = os.path.join(conversation_directory,target+".key")
        if os.path.exists(file):
            with(file,"r") as f:
                key = int(f.read())
                return key
        return None


    def connect_user_to_target(self,user,target):
        conversation_directory = self.get_conversation_directory_name(user,target)
        if not(self._conversation_exists(conversation_directory)):
            os.makedirs(os.path.join(conversation_directory))
            self.initialize_key_share(user,conversation_directory)
        else:
            key = self._check_for_pre_keys(conversation_directory,target)
            if key is not None:
                return key
            else:
                key = self._check_for_selected_pre_key(conversation_directory,target)
                if key is not None:
                    return key
                    

            



    def send_message(self,user,message:str,target:str) -> False:
        pass
            
        #else use ratchet

    def initialize_conversation(self,user,target:str,conversation_directory:str):
        self.initialize_key_share(user,conversation_directory)

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

            





    

