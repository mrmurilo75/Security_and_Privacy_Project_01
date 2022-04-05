import os 

import base64
import hmac

from os import urandom

from binascii import hexlify

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

import timeit

from generator import generate_algo, TEST_FILES_DIR

_MS = 1000
_uS = 1000000

encryption = {
        'aes' : [8, 64, 512, 4096, 32768, 262144, 2047152],
        'rsa' : [2, 4, 8, 16, 32, 64, 128],
        'sha' : [8, 64, 512, 4096, 32768, 262144, 2047152],
    }

key = urandom (32)
iv = urandom (16)

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

def process_sha():
    algo = 'sha'
    digest_times = {}

    for (size , test_files) in generate_algo(algo).items():
        digest_times |= { size : [] }

        for test_file in test_files:
            with open(os.path.join(TEST_FILES_DIR, test_file), 'rb') as ff:
                message = ff.read()
                digest = hashes.Hash(hashes.SHA256())
                hashing = timeit.timeit(lambda: sha_digest(message, digest), number=1)*_uS

            digest_times[size].append( hashing )

    return digest_times

def process_rsa():
    algo = 'rsa'
    encrypt_times = {}
    decrypt_times = {}

    for (size , test_files) in generate_algo(algo).items():
        encrypt_times |= { size : [] }
        decrypt_times |= { size : [] }

        for test_file in test_files:
            with open(os.path.join(TEST_FILES_DIR, test_file), 'rb') as ff:
                message = ff.read()
                private_key = rsa.generate_private_key(
                        public_exponent = 65537,
                        key_size = 2048
                    )
                public_key = private_key.public_key()
                encrypt = timeit.timeit(lambda: rsa_encrypt(message, public_key), number=1)*_uS
                ciphertext = rsa_encrypt(message, public_key)
                decrypt = timeit.timeit(lambda: rsa_decrypt(ciphertext, private_key), number=1)*_uS

            encrypt_times[size].append( encrypt )
            decrypt_times[size].append( decrypt )

    return ( encrypt_times, decrypt_times )

def process_aes():
    algo = 'aes'
    encrypt_times = {}
    decrypt_times = {}

    for (size , test_files) in generate_algo(algo).items():
        encrypt_times |= { size : [] }
        decrypt_times |= { size : [] }

        for test_file in test_files:
            with open(os.path.join(TEST_FILES_DIR, test_file), 'rb') as ff:
                message = ff.read()
                cipher = Cipher( algorithms.AES(key), modes.CTR(iv) )

                encryptor = cipher.encryptor()
                encrypt = timeit.timeit(lambda: aes_encrypt(message, encryptor), number=1)*_uS # Timeit can't see global variables, so the arguments must be passed

                encryptor = cipher.encryptor() # Context finalizes after encryptor is used. Another one has to be generated so we have ciphertext to pass to decryption
                ciphertext = aes_encrypt(message, encryptor)
                decryptor = cipher.decryptor()
                decrypt = timeit.timeit(lambda: aes_decrypt(ciphertext, decryptor), number=1)*_uS

            encrypt_times[size].append( encrypt )
            decrypt_times[size].append( decrypt )

    return ( encrypt_times, decrypt_times )

def print_result(algo, test_times, detailed = False):
    print(algo)
    for size, times in test_times.items():
        avg_c = 0
        avg = 0

        print('\t', size)
        for time in times:
            avg_c += 1
            avg += time
            if detailed:
                print('\n\t\t', time)
        if detailed:
            print('\t\taverage:')

        print('\t\t', avg/avg_c)

def process_all_avg():
    aes_enc, aes_dec = process_aes()
    rsa_enc, rsa_dec = process_rsa()
    sha_dig = process_sha()

    print_result('AES Encryption', aes_enc)
    print_result('AES Decryption', aes_dec)
    print_result('RSA Encryption', rsa_enc)
    print_result('RSA Decryption', rsa_dec)
    print_result('SHA Digest', sha_dig)

if __name__ == '__main__':
    process_all_avg()

