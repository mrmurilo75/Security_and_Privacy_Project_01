import os
import asyncio

import numpy as np
import matplotlib.pyplot as plt

from processor import process_aes, process_rsa, process_sha

async def plot_result(algo, test_times):
    y=[]
    for size, times in test_times.items():
        avg_c = 0
        avg = 0

        for time in times:
            avg_c += 1
            avg += time

        y.append(avg/avg_c)

    fig, ax = plt.subplots()
    plt.grid()

    x = np.arange(len(list(test_times.keys())))
    xlabels = list(test_times.keys())


    ax.plot(x, y, linewidth=2.0)
    ax.set(title = algo,
            xticks=x, xticklabels=xlabels, xlabel="Size (bytes)",
            ylabel="Time (microseconds)")

    plt.show()

def plot_all():
    aes_enc, aes_dec = process_aes()
    rsa_enc, rsa_dec = process_rsa()
    sha_dig = process_sha()

    asyncio.run(plot_result('AES Encryption', aes_enc))
    asyncio.run(plot_result('AES Decryption', aes_dec))
    asyncio.run(plot_result('RSA Encryption', rsa_enc))
    asyncio.run(plot_result('RSA Decryption', rsa_dec))
    asyncio.run(plot_result('SHA Digest', sha_dig))


if __name__ == '__main__':
    plot_all()
