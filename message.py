from datetime import datetime
import json, os
from typing import Tuple,List, TypedDict
import base64

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
    


    def __init__(self,message:bytes,sender:str,recipient:str,sk_data:SK_DATA = None):

        self._timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._message = message
        self._sk_data = sk_data
        self._recipient = recipient
        self._sender = sender

    @classmethod
    def load_json(cls, json_data:str):
        
        data = json.loads(json_data)
        message = cls(base64.b64decode(data["message"]),data["sender"] ,data["recipient"],data["sk_data"])
        message._timestamp = data["timestamp"]
        return message

    def __dict__(self):
        # renvoie un dictionnaire contenant les attributs de l'instance
        return {
            'timestamp': self._timestamp,
            'sk_data': self._sk_data,
            "sender": self._sender,
            "recipient": self._recipient,
            "message": self._message
        }
    
    def __json__(self):
        return {
            'timestamp': self._timestamp,
            'sk_data': self._sk_data,
            "sender": self._sender,
            "recipient": self._recipient,
            "message": self._message
        }

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

    def set_sk_data(self,sk_data:SK_DATA):
        self._sk_data = sk_data

    def set_message(self,message:bytes):
        self._message = message


    def to_json(self):
        return {
            'timestamp': self._timestamp,
            'sk_data': self._sk_data,
            "sender": self._sender,
            "recipient": self._recipient,
            "message": base64.b64encode(self._message).decode('ascii')
            
        }


if __name__ == "__main__":
    message = Message(b"salut","a","b")
    print(message.__dict__())
    json_txt = json.dumps(message)
    m = Message.load_json(json_txt)
    print(m.get_message())