import time, json, os
from typing import Tuple,List

class Message:
    _timestamp:int = None
    _message:bytes = None
    


    def __init__(self,message:bytes):
        self._timestamp = time.time()

        self._message = message


    def get_message_as_json(self):
        return json.dumps({"timestamp: ":self._timestamp," message: ":self._message})

    
class Conversation:
    _targets: Tuple[str,str]
    _messages: List[Message]

    def __init__(self,targets:Tuple[str,str]):
        self._targets = targets
        self._messages = []
        self.load_messages()

    def load_messages(self):
        conversation_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),"server"))
        
        

if __name__ == "__main__":
    c = Conversation(("alice", "bob"))


