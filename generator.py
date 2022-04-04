import string
import random
import os


TEST_FILES_DIR = 'test_files'

algo = {
    "aes" : [8, 64, 512, 4096, 32768, 262144, 2047152],
    "sha" : [8, 64, 512, 4096, 32768, 262144, 2047152],
    "rsa" : [2, 4, 8, 16, 32, 64, 128]
}


def generate(algo):

    if not os.path.isdir(TEST_FILES_DIR):
        os.mkdir(TEST_FILES_DIR)

    for i in range(10):
        for (key, val) in algo.items():
            for size in val:
                ran = "".join(random.choices(string.ascii_lowercase  + string.ascii_uppercase + string.digits, k=size))
                f = open( os.path.join(TEST_FILES_DIR, key + str(i) + "_" + str(size)) , "w" )
                f.write(str(ran))
                f.close()


if __name__ == '__main__': 
    generate(algo)

