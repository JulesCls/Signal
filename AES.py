class AES():
    
    S_BOX =[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16]

    INV_S_BOX = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
                0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
                0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54,
                0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
                0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
                0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8,
                0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
                0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
                0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab,
                0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
                0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
                0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
                0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
                0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
                0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d,
                0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
                0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
                0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 
                0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60,
                0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
                0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
                0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b,
                0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
                0x21, 0x0c, 0x7d]


    def getBlocks(self, input: str | bytes) -> list[bytes]:
        # Convert the string to a bytes object
        if type(input) is str:
            data = input.encode()
        elif type(input) is bytes:
            data = input
        # Initialize an empty list to store the blocks
        blocks = [] 
        # Split the data into blocks of 128 bits (16 bytes)
        for i in range(0, len(data), 16):
            block = data[i:i+16]
            # If the block is not 64 bits long, pad it with 0s
            block = block.ljust(16, b'\x00')
            blocks.append(block)
        return blocks

    #create a matrix of 4x4 bytes using the 16 bytes datas block in input
    def stateInit(self, block: bytes):
        block = bytearray(block)
        state = [[],[],[],[]]
        # convert a block of 16 bytes datas to 4x4 state
        for i in range(4):
            for j in range(4):
                state[i].append(block[j+4*i].to_bytes(1,'big'))
        return state
    
    #convert a state matric into a 16 bytes block
    def state_to_block(self, state: list[list[bytearray]]) -> bytes:
        block = b''
        for i in state:
            row = b''.join(i)
            block += row
        return block

    #each state of the initial state becomes a column
    def transposeState(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        transposedState = [[],[],[],[]]
        for i in range(4):
            for byte in range(4):
                transposedState[i].insert(byte,state[byte][i])
        return transposedState

    def rotWord(self, word: bytes, x: int = 1): #x left rotation of word
        if x == 0 or x == 4:
            return word
        #need 32-bit word bytes object as input
        elif len(word) != 4:
            raise ValueError("Need a 32-bits word to rotate correctly")
        #only rotation 1 to 3 times
        elif not (1 <= x <= 3):
            raise ValueError("only left rotate from 1 to 3 times")
        else:
            res = int.from_bytes(word, 'big')
            b0 = res >> 8*(4-x)
            res &= int("1"*(8*(4-x)),2)
            res = (res << 8*x) | b0
            return res.to_bytes(4,'big')

    def subWord(self, word: bytes): #subsitute word using S_BOX
        #need 32-bit word bytes object as input
        if len(word) != 4:
            raise ValueError("Need a 32-bits word to rotate correctly")
        else:
            #replace each bytes in word by its translation in the S_BOX table
            for i,j in zip(word,range(4)):
                word = word.replace(word[j].to_bytes(1,'big'), self.S_BOX[i].to_bytes(1,'big'))
            return word

    def key_expansion(self, key: int) -> list[bytes]:
        #list that will ocntains the 15 round keys (because of 256 bits original key)
        round_keys = []
        n = 8 # number of 32-bit words in the key
        # round constants
        rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000]
        
        #convert int key in bytes object and then split the key in 32-bits word and add them in the round keys list
        key = key.to_bytes(32,'big')
        for i in range(n):
            round_keys.insert(i,key[4*i:4*(i+1)])
        
        for i in range(8,60):
            #insert w words each 8th such as Wi = Wi-n ^ subword(rotword(Wi-1)) ^ rcon[i//n] 
            if i % 8 == 0:
                round_keys.insert(i, (int.from_bytes(round_keys[i-n],'big') ^ int.from_bytes(self.subWord(self.rotWord(round_keys[i-1])),'big') ^ rcon[(i//n)-1]).to_bytes(4,'big'))
                continue
            #insert w words each 8i+4th such as Wi = Wi-n ^ subword(Wi-1)
            elif i % 4 == 0:
                round_keys.insert(i, (int.from_bytes(round_keys[i-n],'big') ^ int.from_bytes(self.subWord(round_keys[i-1]),'big')).to_bytes(4,'big'))
                continue
            else:
                #insert w words otherwise such as Wi = Wi-n ^ Wi-1
                round_keys.insert(i, (int.from_bytes(round_keys[i-n],'big') ^ int.from_bytes(round_keys[i-1],'big')).to_bytes(4,'big'))     
                continue
        # concatenate 4*32-bits word to get 15*128bits round_key and left rotate again by 4 bytes
        for i in range(0,60,4):
            round_keys[i//4] = b''.join(round_keys[i:i+4])
        round_keys = round_keys[0:15]
        return round_keys

    #this function perform a xor of bytes one by one between a state and a round_key
    def addRoundKey(self, state: list[list[bytearray]], round_keys: bytes) -> list[list[bytearray]]:
        i = 0
        #iteration in each byte of the state
        for line in state:
            for byte in line:
                line[i%4] = (int.from_bytes(byte,'big') ^ round_keys[i]).to_bytes(1,'big')
                i += 1
        return state

    #SubBytes use the same S_BOX as the subWord function, so we loop 4 times to substitute the whole state
    def subBytes(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        i = 0
        for line in state:
            for byte in line:
                #iteration through the whole state and replace the value of bytes by his translations in the INV_S_BOX
                line[i%4] = byte.replace(line[i%4], self.S_BOX[int.from_bytes(byte,'big')].to_bytes(1,'big'))
                i += 1
        return state

    #same function as subBytes but with the INV_S_BOX
    def invSubBytes(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        i = 0
        for line in state:
            for byte in line:
                #iteration through the whole state and replace the value of bytes by his translations in the INV_S_BOX
                line[i%4] = byte.replace(line[i%4], self.INV_S_BOX[int.from_bytes(byte,'big')].to_bytes(1,'big'))
                i += 1
        return state

    #this function cyclically left shifts the bytes in each row by a certain offset. 0 for row 1, 1 for row 2, 2 for row 3 and 3 for row 4
    def shiftRows(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        #define the offset of each shift
        offset = -1
        #index of the state
        i = 0
        for line in state:
            #each state the offset in incremented
            offset += 1
            #we use the rotword function that can performs a shift on a 32-bit word x times
            word = self.rotWord(b''.join(line),offset)
            for _ in line:
                #replace the old word by the new shifted ones and convert to bytes
                line[i%4] = word[i%4].to_bytes(1,'big')
                i += 1
        return state

    #same function as shiftRows but we do a offset of 4-offset to get step back.
    def invShiftRows(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        #define the offset of each shift
        offset = -1
        #index of the state
        i = 0
        for line in state:
            #each state the offset in incremented
            offset += 1
            #we use the rotword function that can performs a shift on a 32-bit word 4-x times
            word = self.rotWord(b''.join(line),4-offset)
            for _ in line:
                #replace the old word by the new shifted ones and convert to bytes
                line[i%4] = word[i%4].to_bytes(1,'big')
                i += 1
        return state

    #perform galois field (2^8) multiplication
    def gmul(self, a, b):
        p = 0
        for i in range(8):
            if (int.from_bytes(b,'big') >> i) & 1:
                p ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x11b
        return p & 0xff

    #perform a matrix multiplication of a column of the state by the below given matrix c
    def mixColumn(self, state: list[bytearray]) -> list[bytearray]:
        c = [[0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]]
        res = []
        for row in c:
            res.append((self.gmul(row[0],state[0]) ^ self.gmul(row[1],state[1]) ^ self.gmul(row[2],state[2]) ^ self.gmul(row[3],state[3])).to_bytes(1,'big'))
        return res
    
    #multiply each colum of state by the matrix c and make the final 4x4 state
    def mixColumns(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        state = self.transposeState(state)
        i = 0
        for line in state:
            state[i] = self.mixColumn(line)
            i += 1
        res = self.transposeState(state)    
        return res
    #perform a matrix multiplication of a column of the state by the below given inverse matrix c
    def invMixColumn(self, state: list[bytearray]) -> list[bytearray]:
        c = [[0x0e, 0x0b, 0x0d, 0x09],
            [0x09, 0x0e, 0x0b, 0x0d],
            [0x0d, 0x09, 0x0e, 0x0b],
            [0x0b, 0x0d, 0x09, 0x0e]]
        res = []
        for row in c:
            res.append((self.gmul(row[0],state[0]) ^ self.gmul(row[1],state[1]) ^ self.gmul(row[2],state[2]) ^ self.gmul(row[3],state[3])).to_bytes(1,'big'))
        return res

    #multiply each colum of state by the inverse matrix c and make the final 4x4 state
    def invMixColumns(self, state: list[list[bytearray]]) -> list[list[bytearray]]:
        state = self.transposeState(state)
        i = 0
        for line in state:
            state[i] = self.invMixColumn(line)
            i += 1
        res = self.transposeState(state)    
        return res

    #encrypt using AES 256 algorithm block by block (use like that for ECB mode)
    def blockEncryption(self, plainTextBlock: bytes, key) -> bytes:
        #test if its a correct sized block in input
        if len(plainTextBlock) != 16:
            raise ValueError("Input must be a 16 bytes block of datas")
        #if ok, initialized the state with the block, and the rounds keys
        state = self.stateInit(plainTextBlock)
        rounds_keys = self.key_expansion(key)
        #init add round key before start looping
        state = self.addRoundKey(state,rounds_keys[0])
        #loop 13 times
        round = 1
        while round <= 13:
            state = self.subBytes(state)
            state = self.shiftRows(state)
            state = self.mixColumns(state)
            state = self.addRoundKey(state,rounds_keys[round])
            round += 1 
        #last round without mix columns
        state = self.subBytes(state)
        state = self.shiftRows(state)
        state = self.addRoundKey(state,rounds_keys[14])
        return self.state_to_block(state)

    #invert of encryption but with the inv functions
    def blockDecryption(self,cypherTextBlock: bytes, key) -> bytes:
        #test if its a correct sized block in input
        if len(cypherTextBlock) != 16:
            raise ValueError("Input must be a 16 bytes block of datas")
        #if ok, initialized the state with the block, and the rounds keys
        state = self.stateInit(cypherTextBlock)
        rounds_keys = self.key_expansion(key)
        #init add round key before start looping and first round without mix columns
        state = self.addRoundKey(state,rounds_keys[14])
        state = self.invShiftRows(state)
        state = self.invSubBytes(state)
        #loop 13 times
        round = 13
        while round > 0:
            state = self.addRoundKey(state,rounds_keys[round])
            state = self.invMixColumns(state)
            state = self.invSubBytes(state)
            state = self.invShiftRows(state)
            round -= 1 
        #last round with round_key[0]
        state = self.addRoundKey(state,rounds_keys[0])
        return self.state_to_block(state)

    #encryption of datas using ECB mode or CBC mode
    def encryption(self, data: bytes, key: int, mode: str, initialVector: bytes = b'\xfd\xdf\xe2i_`\xdcJ\x028\xd1\x8b\x80C]\x89') -> bytes:
        if mode == 'ECB':
            blocks = self.getBlocks(data)
            for block in blocks:
                blocks[blocks.index(block)] = self.blockEncryption(block,key)
            return b''.join(blocks)
        elif mode =='CBC':
            output = []
            blocks = self.getBlocks(data)
            cypherBlock = self.blockEncryption((int.from_bytes(blocks[0],'big') ^ int.from_bytes(initialVector,'big')).to_bytes(16,'big'), key)
            output.append(cypherBlock)
            for i in range(1,len(blocks)):
                output.append(self.blockEncryption((int.from_bytes(blocks[i],'big') ^ int.from_bytes(output[i-1],'big')).to_bytes(16,'big'), key))
            return b''.join(output)

    #decryption of datas using ECB mode or CBC mode
    def decryption(self, cypher: bytes, key: int, mode: str, initialVector: bytes = b'\xfd\xdf\xe2i_`\xdcJ\x028\xd1\x8b\x80C]\x89') -> bytes:
        if mode == 'ECB':
            blocks = self.getBlocks(cypher)
            for block in blocks:
                blocks[blocks.index(block)] = self.blockDecryption(block,key)
            return b''.join(blocks)
        elif mode =='CBC':
            output = []
            blocks = self.getBlocks(cypher)
            plainBlock = (int.from_bytes(self.blockDecryption(blocks[0],key),'big') ^ int.from_bytes(initialVector,'big')).to_bytes(16,'big')
            output.append(plainBlock)
            for i in range(1,len(blocks)):
                output.append((int.from_bytes(self.blockDecryption(blocks[i],key),'big') ^ int.from_bytes(blocks[i-1],'big')).to_bytes(16,'big'))
            return b''.join(output)



if __name__ == "__main__":
    aes = AES()
    key = 23251443973595272567448928302682049732685763840581622945930246895828608753669
    iv = b'\xee'*16
    fp = input("enter filepath: ")
    f = open(fp,'rb')
    data = f.read()
    f.close()
    e = aes.encryption(data,key,'CBC')
    d = aes.decryption(e,key,'CBC')
    
    f = open("res.txt", "wb")
    f.write(d)
    f.close()
   

