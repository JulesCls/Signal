import struct

class SHA256:
    def __init__(self):
        # Initialise les variables nécessaires
        self.h0 = 0x6a09e667
        self.h1 = 0xbb67ae85
        self.h2 = 0x3c6ef372
        self.h3 = 0xa54ff53a
        self.h4 = 0x510e527f
        self.h5 = 0x9b05688c
        self.h6 = 0x1f83d9ab
        self.h7 = 0x5be0cd19

        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b,
            0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
            0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7,
            0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152,
            0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
            0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
            0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819,
            0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08,
            0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f,
            0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

    def _padding(self, message_bytes):
        """
        Ajoute des octets de padding au message binaire
        """
        ml = len(message_bytes) * 8  # Message length in bits
        # Ajoute un '1' à la fin
        message_bytes += b'\x80'

        # Ajoute des zéros jusqu'à ce que le message soit de 448 bits (message_bytes.length*8 + 512 bits)
        while len(message_bytes) % 64 != 56:
            message_bytes += b'\x00'

        # Ajoute la taille du message en bits (64 bits)
        message_bytes += struct.pack(b'>Q', ml)

        return message_bytes

    def _split_chunks(self, padded_message):
        """
        Divise le message en chunks de 512 bits
        """
        # Découpe le message en chunks de 64 octets (64*8=512)
        chunks = [padded_message[i:i+64] for i in range(0, len(padded_message), 64)]
        return chunks

    def _get_words(self, chunk):
        """
        Convertit un chunk de 64 octets en 16 mots de 32 bits
        """
        # Découpe le chunk en 16 mots de 32 bits
        words = struct.unpack(b'>16L', chunk)
        return list(words)

    def _extend_words(self, words):
        """
        Étend la liste des mots de 16 à 64
        """
        for i in range(16, 64):
            s0 = self._right_rotate(words[i-15], 7) ^ \
                self._right_rotate(words[i-15], 18) ^ (words[i-15] >> 3)
            s1 = self._right_rotate(words[i-2], 17) ^ \
                self._right_rotate(words[i-2], 19) ^ (words[i-2] >> 10)
            words.append((words[i-16] + s0 + words[i-7] + s1) & 0xffffffff)
        return words

    def _right_rotate(self, n, d):
        """
        Effectue un rotation de n à droite de d bits
        """
        return (n >> d) | (n << (32 - d)) & 0xffffffff

    def _compress(self, words):
        """
        Compresse 512 bits en 256
        """
        a, b, c, d, e, f, g, h = self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7

        for i in range(64):
            s1 = self._right_rotate(e, 6) ^ self._right_rotate(e, 11) ^ \
                 self._right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + s1 + ch + self.k[i] + words[i]) & 0xffffffff
            s0 = self._right_rotate(a, 2) ^ self._right_rotate(a, 13) ^ \
                 self._right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xffffffff

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

        self.h0 = (self.h0 + a) & 0xffffffff
        self.h1 = (self.h1 + b) & 0xffffffff
        self.h2 = (self.h2 + c) & 0xffffffff
        self.h3 = (self.h3 + d) & 0xffffffff
        self.h4 = (self.h4 + e) & 0xffffffff
        self.h5 = (self.h5 + f) & 0xffffffff
        self.h6 = (self.h6 + g) & 0xffffffff
        self.h7 = (self.h7 + h) & 0xffffffff

    def _hexdigest(self):
        """
        Retourne l'empreinte hexadécimale
        """
        return '{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}'.format(self.h0, self.h1, self.h2, self.h3,self.h4, self.h5, self.h6, self.h7)

    def digest(self, message_bytes):
        return bytes.fromhex(self.hexdigest(message_bytes))

    def arraydigest(self,message_bytes):
        return bytearray.fromhex(self.hexdigest(message_bytes))
    
    def update(self, data):
        data = self.padding(data)
        blocks = self.to_blocks(data)
        for block in blocks:
            self.process_block(block)

    
    def hexdigest(self, message_bytes):
        self.h0 = 0x6a09e667
        self.h1 = 0xbb67ae85
        self.h2 = 0x3c6ef372
        self.h3 = 0xa54ff53a
        self.h4 = 0x510e527f
        self.h5 = 0x9b05688c
        self.h6 = 0x1f83d9ab
        self.h7 = 0x5be0cd19
        """
        Retourne l'empreinte hexadecimale SHA256 du message binaire passé en paramètre
        """
        # Ajoute des octets de padding au message binaire
        padded_message = self._padding(message_bytes)

        # Découpe le message en chunks de 512 bits
        chunks = self._split_chunks(padded_message)

        # Traitement des chunks
        for chunk in chunks:
            # Convertit le chunk en mots de 32 bits
            words = self._get_words(chunk)

            # Étend la liste des mots à 64
            words = self._extend_words(words)

            # Compresse 512 bits en 256
            self._compress(words)

        # Retourne le bytearray de l'empreinte hexadécimale
        return self._hexdigest()

import hashlib

if __name__ == "__main__":
    
    test = "sdjfhsdkfhj&é-èçà__çè_ç-è-(yiugshjkfnslkef usfhj kdsfhl ezuify è_-_èf (-sdçfè a_zfy ze))"
    test = test.encode()

    sha = SHA256()
    m = hashlib.sha256()
    m.update(test)



    res1 = sha.digest(test)
    res2 = sha.hexdigest(test)
    res3 = sha.hexdigest(test)
    print(res1)
    print(res2)
    print(res3)
    print(res1 == m.digest())

    
    