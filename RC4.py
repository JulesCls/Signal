class RC4:
    S = []

    def __init__(self,key:bytes) -> None:
        self.S = [i for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def __generate_random_flow(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[(self.S[i] + self.S[j]) % 256]
            yield K

    def encrypt(self, plain_text:bytes):
        generator = self.__generate_random_flow()
        cipher_text:bytearray = []
        for char in plain_text:
            cipher_text.append(char ^ next(generator))
        return bytes(cipher_text)

    def decrypt(self, cipher_text:bytes):
        return self.encrypt(cipher_text)
        


if __name__ == "__main__":
    print(ord("1"))
    key = 1234567891286189264389127409812749871264897612890471298487120948120984
    key = key.to_bytes(256,"big")
    rc4 = RC4(key)
    plain_text = b"This is a secret message"

    cipher_text = rc4.encrypt(plain_text)
    print(cipher_text)

    rc4 = RC4(key)
    decrypted_text = rc4.decrypt(cipher_text)
    print(decrypted_text.decode())
