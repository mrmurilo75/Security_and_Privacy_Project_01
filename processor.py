import base64
import hmac

from os import urandom

from binascii import hexlify

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

import timeit


key = urandom (32)
iv = urandom (16)

# print( hexlify(key), hexlify(iv) )

def aes_encrypt(message, encryptor):
    return encryptor.update(message) + encryptor.finalize()

def aes_decrypt(ciphertext, decryptor):
    return decryptor.update(ciphertext) + decryptor.finalize()

def rsa_encrypt(message, key):
    return key.encrypt(
            message,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
def rsa_decrypt(ciphertext, key):
    return key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

def sha_digest(message, digest):
    digest.update(message)
    digest.finalize()

encryption = {
        'aes' : [8, 64, 512, 4096, 32768, 262144, 2047152],
        'rsa' : [2, 4, 8, 16, 32, 64, 128],
        'sha' : [8, 64, 512, 4096, 32768, 262144, 2047152],
    }

for enc, val in encryption.items():
    for leng in val:

        encrypt = 0
        decrypt = 0
        hashing = 0

        for i in range(10):

            with open(enc + str(i) +'_' + str(leng), 'rb') as ff:
                message = ff.read()
                if enc == 'aes' :
                    cipher = Cipher( algorithms.AES(key), modes.CTR(iv) )
                    encryptor = cipher.encryptor()
                    encrypt += timeit.timeit(lambda: aes_encrypt(message, encryptor), number=1) # Timeit can't see global variables, so the arguments must be passed
                    encryptor = cipher.encryptor() # Context finalizes after encryptor is used. Another one has to be generated so we have ciphertext to pass to decryption
                    ciphertext = aes_encrypt(message, encryptor)
                    decryptor = cipher.decryptor()
                    decrypt += timeit.timeit(lambda: aes_decrypt(ciphertext, decryptor), number=1)
                    decryptor = cipher.decryptor()
                    decrypted = aes_decrypt(ciphertext, decryptor)
                elif enc == 'rsa' :
                    private_key = rsa.generate_private_key(
                            public_exponent = 65537,
                            key_size = 2048
                        )
                    public_key = private_key.public_key()
                    encrypt += timeit.timeit(lambda: rsa_encrypt(message, public_key), number=1)
                    ciphertext = rsa_encrypt(message, public_key)
                    decrypt += timeit.timeit(lambda: rsa_decrypt(ciphertext, private_key), number=1)
                elif enc == 'sha' :
                    digest = hashes.Hash(hashes.SHA256())
                    hashing += timeit.timeit(lambda: sha_digest(message, digest), number=1)

                    




        if(hashing != 0):
            hashing *= 100000
            print('sha digestion ' + str(leng) + '\t ', hashing)
        else:
            encrypt *= 100000
            print(enc + ' encryption ' + str(leng) + '\t ', encrypt)
            decrypt *= 100000
            print(enc + ' decryption ' + str(leng) + '\t ', decrypt)


