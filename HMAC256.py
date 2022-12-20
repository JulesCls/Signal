from sha256 import SHA256

class HMAC256:

    @staticmethod
    def hexdigest(key:bytearray,message:bytearray):
        sha256 = SHA256()
        
        if len(key) < 64:
            key += b'\x00' * (64 - len(key))
        elif len(key) > 64:
            key = sha256.digest(key)

        
        # Create array of byte from key
        k1 = bytearray(key)
        k2 = bytearray(key)
        
        for i in range(64): #xor each byte
            k1[i] ^= 0x36 #ipad
            k2[i] ^= 0x5c #opad
        
        
        h1 = sha256.digest(k1 + message)
        hmac_hash = sha256.hexdigest(k2 + h1)

        # Return hash in hex format
        return hmac_hash

    @staticmethod
    def digest(key:bytearray,message:bytearray):
        return bytes.fromhex(HMAC256.hexdigest(key,message)) #return hash in bytes format

    @staticmethod
    def arraydigest(key:bytearray,message:bytearray):
        return bytearray.fromhex(HMAC256.hexdigest(key,message)) #return hash in bytearray format


if __name__ == "__main__":
    key ="a key".encode()
    message = 'my message'.encode()
    print(HMAC256.digest(key,message))