import string
import random
import sys


algo = {
    "aes" : [8, 64, 512, 4096, 32768, 262144, 2047152],
    "sha" : [8, 64, 512, 4096, 32768, 262144, 2047152],
    "rsa" : [2, 4, 8, 16, 32, 64, 128]
}


def runCode(algo):
    for i in range(10):
        for item in algo:
            ran = "".join(random.choices(string.ascii_lowercase  + string.ascii_uppercase + string.digits, k=size))
            f = open(str(algo) + i + "_" + str(size), "w")
            f.write(str(ran))
            f.close()

