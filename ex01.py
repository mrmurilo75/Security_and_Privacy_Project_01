import hmac

from os import urandom

from binascii import hexlify

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import timeit


key = urandom (32)
iv = urandom (16)

# print( hexlify(key), hexlify(iv) )


encryption = ['aes', 'sha', 'rsa']
length = {
        'aes' : [8, 64, 512, 4096, 32768, 262144, 2047152],
        'sha' : [8, 64, 512, 4096, 32768, 262144, 2047152],
        'rsa' : [2, 4, 8, 16, 32, 64, 128],
    }

for enc in encryption:
    for leng in length[enc]:

        encryptor = Cipher( algorithms.AES(key), modes.CTR(iv) ).encryptor()

        with open(enc + str(leng), 'rb') as ff:

            print( timeit.timeit(lambda: encryptor.update(ff.read()) + encryptor.finalize(), number=1) )

