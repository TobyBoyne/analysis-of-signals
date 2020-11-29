import numpy as np
import matplotlib.pyplot as plt

from window.window_funcs import *
from animate import GroupAnimator, WindowFuncAnimator
import read_data

# signal functions
def sine_sweep(ts):
	"""Return a function that generates a pure sine wave of frequency k"""
	return lambda k: np.sin(2 * np.pi * k * ts)

def real_signal(data):
	"""Return a function that gives a sample of a real signal"""
	pass

if __name__ == '__main__':
	N = 1000
	total_time = 20.
	T = total_time / N

	ts = np.linspace(0., total_time, N)
	fs = np.linspace(0., 1. / (2. * T), N // 2)

	fig, all_axes = plt.subplots(nrows=2, ncols=4, sharey='row', figsize=(15, 10))

	windows = (rectangular, triangular, hann, flat_top)
	# signal = lambda k: np.sin(2 * np.pi * k * ts / 4)

	real_data = read_data.load_sweep('300')
	signal = sine_sweep(ts)

	anims = []
	for ax_pair, window_func in zip(all_axes.T, windows):
		anim = WindowFuncAnimator(ax_pair, window_func, signal, ts, fs,
						plot_window=True)
		anims.append(anim)

	grp = GroupAnimator(fig, anims, 5)
	fig.legend(('Signal', 'Window Function'))
	# grp.save('window_sine_sweep.gif', 'ffmpeg')
	plt.show()
