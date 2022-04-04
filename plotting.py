import os

import numpy as np
import matplotlib.pyplot as plt

from processor import process_aes, process_rsa, process_sha


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


def main():
    aes_enc, aes_dec = process_aes()
    rsa_enc, rsa_dec = process_rsa()
    sha_dig = process_sha()


if __name__ == '__main__':
    main()


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

