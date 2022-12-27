from datetime import datetime
import json, os
from typing import Tuple,List, TypedDict

class sk_data(TypedDict):
    otpk:int
    ephermal:int

class Message:
    _timestamp:int = None
    _sk_data:sk_data = None
    _message:bytes = None
    


    def __init__(self,message:bytes,sk_data:sk_data = None):
        self._timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._message = message
        self._sk_data = sk_data

    def __init__(self, json_data:str) -> None:
        data = json.loads(json_data)
        data["timestamp"] = self._timestamp
        data["sk_data"] = self._sk_data
        data["message"] = self._message

    def get_sk_data(self):
        return self._sk_data


    def get_message_as_json(self):
        return json.dumps({"timestamp":self._timestamp,"message":self._message})


