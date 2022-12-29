import json, utils, os, random
from typing import Tuple, List, TypedDict
from message import Message


class user_messages(TypedDict):
    target:str
    messages:List[Message]


    

class Server:
    _instance = None
    _public_prime = None
    _public_generator = None
    _numbers_in_cache = False
    _server_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"server"))
    _server_messages:user_messages = {}


    _public_info_storage = "pub.json"

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
        with open(os.path.join(self._server_directory_path,self._public_info_storage),"r") as f:
            data = json.loads(f.read())
            self._public_prime = data["prime_number"]
            self._public_generator = data["generator_element"]
        if None in [self._public_generator,self._public_prime]:
            raise Exception("Le nom de fichier contenant les nombres publics du démarrage sont incorrectes ou bien le format n'est pas respecté.")
        

    def _generate_new_public_numbers(self): #generate p prime number and g a generator that will be used for next uses as public information of the server
        p_g = utils.get_number_with_generator_element()
        with open(self._public_info_storage,"w") as f:
            f.write(json.dumps(p_g))
        print("Generation done.")

    def share_public_info_target_to_user(self,target:str): #retrieve public information of a user on the server and chose one otpk key from him
        data = self.get_public_info_of_user(target)
        otpk = random.choice(data["otpk"])
        data["otpk"] = otpk
        self._remove_otpk_stored_from_target(target,otpk)
        return data

    def _remove_otpk_stored_from_target(self,target:str,otpk:int): #remove the user otpk choses previously that is stored on the server
        file = os.path.join(self._server_directory_path,target+".json")
        data = None
        with open(file,"r") as f:
            data = json.loads(f.read())
        data["otpk"].remove(otpk)
        with open(file,'w') as f:
            f.write(json.dumps(data))


    def get_public_info_of_user(self,username): #load information of a user on the server
        file = os.path.join(self._server_directory_path,username+".json")
        if os.path.exists(file):
            with open(file,"r") as f:
                    return json.loads(f.read())
        raise Exception("Utilisateur introuvable.")

    def get_id_of_user(self,username): #return the id of the user on the server
        return self.get_public_info_of_user(username)["id"]

        
    def publish_user_info(self,user): #save the information of a user on the server
        file = os.path.join(self._server_directory_path,user.get_name()+".json")
        with open(file,"w") as f:
            f.write(json.dumps(user.share_info_to_server()))

    def update_user_info(self,user): #used to update pk if user has changed it
        try:
            data = self.get_public_info_of_user(user.get_name())
            if len(data["otpk"]) < 10:
                user.generate_otpk()
                self.publish_user_info(user)
            if data["pk"] != user.share_info_to_server()["pk"]:
                self.publish_user_info(user)
        except:
            self.publish_user_info(user)

    def connect_user(self,user): #connect a user to the server
        self.update_user_info(user)

    def get_user_messages_from_target(self,user,target) -> List[Message]: #retrive a list of messages destined to a user from another user
        messages = self.read_messages_from_file()
        name = user.get_name()
        if name in messages.keys():
            data = []
            for message in messages[name]:
                if message.get_sender() == target:
                    data.append(message)
            for message in data:
                messages[name].remove(message)
            self.write_messages_to_file(messages)
            return data
        return []

    def send_message(self,message:Message) -> False: #add message to the message.json file on the server
        messages = self.read_messages_from_file()
        if message.get_recipient() in messages.keys():
            messages[message.get_recipient()].append(message)
        else:
            messages[message.get_recipient()] = [message]
        self.write_messages_to_file(messages)
            


    def write_messages_to_file(self,messages:user_messages): #save messages to file message.json on the server
        file = os.path.join(self._server_directory_path,"messages.json")
        with open(file,"w") as f:
            f.write(json.dumps(messages))
        
    def read_messages_from_file(self)->user_messages:
        server_messages = {}
        file = os.path.join(self._server_directory_path,"messages.json")
        if os.path.exists(file):
            with open(file,"r") as f:
                data = json.loads(f.read())
                for user in data.keys():
                    server_messages[user] = []
                    for message in data[user]:
                        server_messages[user].append(Message.load_json(json.dumps(message)))
            return server_messages
        else:
            return {}
