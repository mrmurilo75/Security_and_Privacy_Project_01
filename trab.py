import string
import random

aes = [8, 64, 512, 4096, 32768, 262144, 2047152]
sha = [8, 64, 512, 4096, 32768, 262144, 2047152]
rsa = [2, 4, 8, 16, 32, 64, 128]

for size in aes:
    ran = "".join(random.choices(string.ascii_lowercase  + string.ascii_uppercase + string.digits, k=int(size/4)))
    f = open("aes" + str(size), "w")
    f.write(str(ran))
    f.close()

for size in sha:
    ran = "".join(random.choices(string.ascii_lowercase  + string.ascii_uppercase + string.digits, k=int(size/4)))
    f = open("sha" + str(size), "w")
    f.write(str(ran))
    f.close()

for size in rsa:
    ran = "".join(random.choices(string.ascii_lowercase  + string.ascii_uppercase + string.digits, k=int(size/4)))
    f = open("rsa" + str(size), "w")
    f.write(str(ran))
    f.close()
