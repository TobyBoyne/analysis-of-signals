import numpy as np
import matplotlib.pyplot as plt

from window.window_funcs import *
from animate import GroupAnimator, Animator


if __name__ == '__main__':
	N = 1000
	total_time = 20.
	T = total_time / N

	ts = np.linspace(0., total_time, N)
	fs = np.linspace(0., 1. / (2. * T), N // 2)

	fig, all_axes = plt.subplots(nrows=2, ncols=4, sharey='row')

	windows = (rectangular, triangular, hann, flat_top)
	signal = lambda k: np.sin(2 * np.pi * k * ts / 4)

	anims = []
	for ax_pair, window_func in zip(all_axes.T, windows):
		anim = Animator(ax_pair, window_func, signal, ts, fs)
		anims.append(anim)

	grp = GroupAnimator(fig, anims, 5)
	plt.show()
