from sha256 import Sha256
import primalNumber,utils


def HMAC_256(key:int,m:int):
    sha256 = Sha256()
    opad = 0x5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c
    ipad = 0x3636363636363636363636363636363636363636363636363636363636363636
    print(len(bin(ipad)))

    if len(bin(key)[2:]) > 256:
        key = sha256.int_hash(key)
    while(len(bin(key)[2:0]) > 256):
        key <<= 1

    left_operation = key ^ opad
    right_operation = sha256.int_hash((key ^ ipad) | m)

    return sha256.int_hash(left_operation | right_operation)

if __name__ == "__main__":
    sha256 = Sha256()
    key = 1347970089728574169630159058194593715446431332080111800307126033557879564623561271064755333325920715118756313806805813307389675662594418400047194434929731
    message = "hello je suis un message"
    print(message)
    message = utils.mergeBinaryString(message)
    print(message)
    print(utils.unMergeBinaryString(message))
    print(hex(HMAC_256(key,message)))


    key = utils.unMergeBinaryString(key).encode()
    message = 'my message'.encode()
    import hashlib
    import hmac
    hmac_obj = hmac.new(key, message,hashlib.sha256)
    print(hmac_obj.hexdigest())