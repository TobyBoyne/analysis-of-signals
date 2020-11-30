import numpy as np
import matplotlib.pyplot as plt

from animate import GroupAnimator, Animator, INTERVAL
from window.window_funcs import *

def get_scaling_window(window_size, t_size):
	def window(t_start):
		w = np.zeros(t_size)
		w[t_start:t_start+window_size] = 1.
		return w
	return window



class SampleTimeAnimator(Animator):
	def __init__(self, axes, signal_func, ts, fs, window_func, window_size, **kwargs):
		super().__init__(axes, None, signal_func, ts, fs, **kwargs)

		self.signal = signal_func()

		self.ax_time.set_xlim(0, np.max(ts))
		self.ax_time.set_ylim(-1, 1)

		self.ax_freq.set_xlim(0, 10)
		self.ax_freq.set_ylim(0, 1.5)

		self.line_time.set_linestyle('--')
		self.line_time.set_alpha(0.5)

		self.sampled_line, = self.ax_time.plot([], [], color='tab:blue', lw=3)

		self.window_func = window_func
		self.window_line, = self.ax_time.plot(ts, window_func(0))

		wavelengths = fr'$=\frac{{{window_size//50}}}{{2}}$'
		self.ax_time.set_title(f'Window size{wavelengths} wavelengths')

		self.window_size = window_size
		# find the number of times each cycle needs to be repeated
		self.repeat_samples = int(np.ceil(len(ts) / window_size))

		# plot the real frequency
		self.real_freq_line = self.ax_freq.vlines(1, 1e-5, 1, color='tab:green', lw=3, linestyle='--')

	def repeat_sample(self, wave, offset):
		"""For a sample of the wave, repeat it for the entire range of ts"""
		sample = wave[offset:offset + self.window_size]
		full_wave = np.roll(np.tile(sample, self.repeat_samples), offset)[:len(self.ts)]
		return sample, full_wave


	def evaluate(self, i):
		"""Signal is to be evaluated for ts"""
		k = i * 3

		window = self.window_func(k)

		windowed_wave = self.signal * window
		sample, full_wave = self.repeat_sample(windowed_wave, k)
		self.y_time = full_wave
		self.line_time.set_ydata(self.y_time)

		self.sampled_line.set_data(self.ts[k:self.window_size+k], sample)

		fft = np.fft.fft(self.y_time)
		self.y_freq = 2. / N * np.abs(fft[0:N // 2])
		self.line_freq.set_ydata(self.y_freq)

		self.window_line.set_ydata(window)

		return [self.line_time, self.line_freq, self.window_line]

if __name__ == '__main__':
	N = 1000
	total_time = 10.
	T = total_time / N

	ts = np.linspace(0., total_time, N)
	fs = np.linspace(0., 1. / (2. * T), N // 2)

	fig, all_axes = plt.subplots(nrows=2, ncols=3, sharey='row', figsize=(15, 10))
	signal = lambda: np.sin(2 * np.pi * ts)
	window_sizes = (50, 350, 650)

	anims = []
	for ax_pair, window_size in zip(all_axes.T, window_sizes):
		window_func = get_scaling_window(window_size, len(ts))
		anim = SampleTimeAnimator(ax_pair, signal, ts, fs, window_func, window_size,
								  log_amplitude=False)
		anims.append(anim)

	handles = (anim.line_freq, anim.window_line, anim.real_freq_line)
	fig.legend(handles, ('Signal', 'Sampled region', 'Real frequency'))

	grp = GroupAnimator(fig, anims, 3)
	grp.save('sample_time_sine.gif', writer='ffmpeg')
	plt.show()

