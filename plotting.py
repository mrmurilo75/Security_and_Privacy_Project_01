import os
import asyncio

import numpy as np
import matplotlib.pyplot as plt

from processor import process_aes, process_rsa, process_sha


async def plot_result(algo, test_times):
    x=[]
    y=[]
    max_key = 0
    max_time = 0
    for size, times in test_times.items():
        x.append(size)
        avg_c = 0
        avg = 0

        for time in times:
            avg_c += 1
            avg += time

        y.append(avg/avg_c)

    # plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()

    x = np.arange(len(list(test_times.keys())))
    xlabels = list(test_times.keys())

    print(xlabels)
    # print(xlist)

    ax.plot(x, y, linewidth=2.0)
    ax.set(title = algo,
            xticks=x, xticklabels=xlabels, xlabel="Syze (in bytes)",
            ylabel="Time (in microseconds)") #yticks=np.arange(1, max_time, max_time/10))

    #ax.set(xlim = (0,8), xticks=test_times.keys(), 
            #ylim = (0,8), yticks=np.arrange(1, 8))

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


"""
# example from https://matplotlib.org/stable/gallery/lines_bars_and_markers/errorbar_subsample.html#sphx-glr-gallery-lines-bars-and-markers-errorbar-subsample-py

# example data
x = np.arange(0.1, 4, 0.1)
y1 = np.exp(-1.0 * x)
y2 = np.exp(-0.5 * x)

# example variable error bar values
y1err = 0.1 + 0.1 * np.sqrt(x)
y2err = 0.1 + 0.1 * np.sqrt(x/2)


fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, sharex=True,
                                    figsize=(12, 6))

ax0.set_title('all errorbars')
ax0.errorbar(x, y1, yerr=y1err)
ax0.errorbar(x, y2, yerr=y2err)

ax1.set_title('only every 6th errorbar')
ax1.errorbar(x, y1, yerr=y1err, errorevery=6)
ax1.errorbar(x, y2, yerr=y2err, errorevery=6)

ax2.set_title('second series shifted by 3')
ax2.errorbar(x, y1, yerr=y1err, errorevery=(0, 6))
ax2.errorbar(x, y2, yerr=y2err, errorevery=(3, 6))

fig.suptitle('Errorbar subsampling')
plt.show()
"""

