from datetime import datetime
import json, os
from typing import Tuple,List, TypedDict
import base64

'''
Méthode _default récupérée sur stack overflow, utilisée pour changer les méthodes de bases utilisées par json.dumps(), cela permet de sérialiser la classe.
'''
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.



class SK_DATA(TypedDict):
    otpk:int
    ephermal:int
    signature:Tuple[int,int]

class Message:
    _timestamp:int = None
    _sk_data:SK_DATA = None
    _message:bytes = None
    _sender:str = None
    _recipient:str = None
    _filepath:str = None
    


    def __init__(self,message:bytes,sender:str,recipient:str,filepath: str, sk_data:SK_DATA = None):
        self._timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._message = message
        self._sk_data = sk_data
        self._recipient = recipient
        self._sender = sender
        self._filepath = filepath

    @classmethod
    def load_json(cls, json_data:str): #permet de lire une chaine de caractères JSON et d'ensuite créer une instance de l'objet message
        data = json.loads(json_data)
        message = cls(base64.b64decode(data["message"]),data["sender"] ,data["recipient"],data['filepath'],data["sk_data"])
        message._timestamp = data["timestamp"]
        return message

    def get_sk_data(self) -> SK_DATA:
        return self._sk_data

    def get_sender(self) -> str:
        return self._sender

    def get_recipient(self) -> str:
        return self._recipient
    
    def get_timestamp(self) -> str:
        return self._timestamp

    def get_message(self) -> bytes:
        return self._message
    
    def get_filepath(self) -> str:
        return self._filepath

    def set_sk_data(self,sk_data:SK_DATA):
        self._sk_data = sk_data

    def set_message(self,message:bytes):
        self._message = message

    def clear_for_write(self):
        self._sk_data = None


    def to_json(self): #retourner un objet au format JSON
        return {
            'timestamp': self._timestamp,
            'sk_data': self._sk_data,
            "sender": self._sender,
            "recipient": self._recipient,
            "message": base64.b64encode(self._message).decode('ascii'),
            "filepath": self._filepath
        }


if __name__ == "__main__":
    message = Message(b"salut","a","b")
    print(message.__dict__())
    json_txt = json.dumps(message)
    m = Message.load_json(json_txt)
    print(m.get_message())