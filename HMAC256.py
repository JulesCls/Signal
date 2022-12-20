from sha256 import Sha256
from newsha256 import SHA256
import primalNumber,utils, struct
from decimal import Decimal


def HMAC_256(key:int,m:int):
    sha256 = Sha256()
    opad = 0x5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c
    ipad = 0x3636363636363636363636363636363636363636363636363636363636363636

    if len(bin(key)[2:]) > 256:
        key = sha256.int_hash(key)
    else:
        key = key << (256 - len(bin(key)[2:]) - 1)

    k1 = ipad^key
    k2 = opad^key


    h1 =  sha256.int_hash(str(k1) + str(m))
    hmac = sha256.int_hash(str(k2) + str(h1))

    return hmac



import hashlib

def compute_hmac(key, message):
    # Si la clé est plus courte que la longueur du bloc de l'algorithme de hachage (64 octets pour SHA256), elle doit être étendue
    if len(key) < 32:
        key += b'\x00' * (32 - len(key))
    elif len(key) > 32:
        key = hashlib.sha256(key).digest()

    
    # Créer deux pads de clé, K1 et K2
    k1 = bytearray(key)
    k2 = bytearray(key)
    
    for i in range(32):
        k1[i] ^= 0x36
        k2[i] ^= 0x5c
    
    
    h1 = hashlib.sha256(k1 + message).digest()
    hmac_hash = hashlib.sha256(k2 + h1).hexdigest()

    # Retournez le hachage sous forme de chaîne hexadécimale
    return hmac_hash

if __name__ == "__main__":
    sha256 = Sha256()
    key = utils.mergeBinaryString('my key')
    message = "my message"
    message = utils.mergeBinaryString(message)
    print(hex(HMAC_256(key,message)))
    print(hex(HMAC_256(key,message)))


    key = utils.unMergeBinaryString(key).encode('utf-16-be')
    message = 'my message'.encode('utf-16-be')
    print(compute_hmac(key,message))
    
    # import hashlib
    # import hmac
    # hmac_obj = hmac.new(key, message,hashlib.sha256)
    # print(hmac_obj.hexdigest())