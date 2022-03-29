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

result = b''
def encrypt_result():
    result = (encryptor.update(ff.read()) + encryptor.finalize())

ciphertext = ''
def rsa_ciphertext():
    ciphertext = public_key.encrypt(
            ff.read(),
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
def rsa_deciphertext():
    private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

encryption = {
        'aes' : [8, 64, 512, 4096, 32768, 262144, 2047152],
        'sha' : [8, 64, 512, 4096, 32768, 262144, 2047152],
        'rsa' : [2, 4, 8, 16, 32, 64, 128],
    }

for enc, val in encryption.items():
    for leng in val:

        encrypt = 0
        decrypt = 0

        for i in range(10):

            with open(enc + str(i) +'_' + str(leng), 'rb') as ff:

                if enc == 'aes' :
                    cipher = Cipher( algorithms.AES(key), modes.CTR(iv) )
                    encryptor = cipher.encryptor()
                    decryptor = cipher.decryptor()
                    encrypt += timeit.timeit(encrypt_result, number=1)
                    decrypt += timeit.timeit(lambda: decryptor.update(result) + decryptor.finalize(), number=1)
                elif enc == 'sha' :
                    pass
                elif enc == 'rsa' :
                    private_key = rsa.generate_private_key(
                            public_exponent = 65537,
                            key_size = 2048
                        )
                    public_key = private_key.public_key()
                    print('here')
                    encrypt += timeit.timeit(rsa_ciphertext, number=1)
                    decrypt += timeit.timeit(rsa_deciphertext, number=1)





        encrypt *= 100000
        print(enc + ' encryption ' + str(leng) + '\t ', encrypt)
        decrypt *= 100000
        print(enc + ' decryption ' + str(leng) + '\t ', decrypt)


