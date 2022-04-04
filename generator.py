import string
import random
import os


_TEST_FILES_DIR = 'test_files'
TEST_FILES_DIR = _TEST_FILES_DIR if os.path.isdir(_TEST_FILES_DIR) else (os.mkdir(_TEST_FILES_DIR) or _TEST_FILES_DIR)

TEST_LIMIT = 10

algo = {
    "aes" : [8, 64, 512, 4096, 32768, 262144, 2047152],
    "sha" : [8, 64, 512, 4096, 32768, 262144, 2047152],
    "rsa" : [2, 4, 8, 16, 32, 64, 128]
}

def _generate_string(size): 
    return "".join(random.choices(string.ascii_lowercase  + string.ascii_uppercase + string.digits, k=size))

def generate_algo(key):
    generated_files = {}

    for size in algo[key]:
        generated_files |= { size : [] }

        for i in range(TEST_LIMIT):
            ran = _generate_string(size)
            test_file = key + "_t" + str(i) + "_s" + str(size)

            with open( os.path.join(TEST_FILES_DIR, test_file) , "w" ) as ff:
                ff.write( str(ran) )

            generated_files[size].append(test_file) 

    return generated_files


def generate(algo):
    for key in algo:
        generate_algo(key)


if __name__ == '__main__': 
    generate(algo)

