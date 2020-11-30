import numpy as np
import matplotlib.pyplot as plt

from window.window_funcs import *
from animate import GroupAnimator, Animator, INTERVAL
import read_data

# signal functions
def sine_sweep(ts):
	"""Return a function that generates a pure sine wave of frequency k"""
	return lambda k: np.sin(2 * np.pi * k * ts)

def real_signal(data):
	"""Return a function that gives a sample of a real signal"""
	pass


class WindowFuncAnimator(Animator):
	def __init__(self, axes, window_func, signal_func, ts, fs, **kwargs):
		super().__init__(axes, window_func, signal_func, ts, fs, **kwargs)
		self.ax_time.plot(ts, self.window)

		self.ax_time.set_xlim(0, np.max(ts))
		self.ax_time.set_ylim(-1, 1)

		self.ax_freq.set_xlim(0, 2)
		if kwargs.get('log_amplitude', False):
			self.ax_freq.set_ylim(1e-4, 2e0)
		else:
			self.ax_freq.set_ylim(0, 1.5)

	def evaluate(self, i):
		k = (i + 10) * (INTERVAL / 1000) / 4
		N = len(self.ts)

		self.y_time = self.signal(k) * self.window
		self.line_time.set_ydata(self.y_time)

		fft = np.fft.fft(self.y_time)
		self.y_freq = 2. / N * np.abs(fft[0:N // 2])
		self.line_freq.set_ydata(self.y_freq)

		return [self.line_time, self.line_freq]

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
						plot_window=True, log_amplitude=True)
		anims.append(anim)

	grp = GroupAnimator(fig, anims, 5)
	fig.legend(('Signal', 'Window Function'))
	grp.save('window_log_sweep.gif', 'ffmpeg')
	plt.show()
