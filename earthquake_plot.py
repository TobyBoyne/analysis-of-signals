import numpy as np
import matplotlib.pyplot as plt

from read_data import load_earthquake
from animate import Animator, GroupAnimator, INTERVAL
from window.window_funcs import hann, flat_top

def get_window(window_size, window_func, t_size):
	def window(t_start):
		w = np.zeros(t_size)
		window_region = np.arange(window_size)
		w[t_start:t_start+window_size] = window_func(window_region)
		return w
	return window


class EarthquakeAnimator(Animator):
	def __init__(self, axes, signal_func, ts, fs, window_func, window_size, total_frames, **kwargs):
		super().__init__(axes, None, signal_func, ts, fs, **kwargs)

		self.signal = signal_func()

		self.ax_time.set_xlim(0, np.max(ts))
		self.ax_time.set_ylim(-2, 2)

		self.ax_freq.set_xlim(0, 100)
		self.ax_freq.set_ylim(1e-3, 1.5)

		self.line_time.set_linewidth(2)
		self.line_time.set_linestyle('--')
		self.line_time.set_alpha(0.5)

		self.line_freq.set_linewidth(1)

		self.sampled_line, = self.ax_time.plot([], [], color='tab:blue', lw=3)

		self.window_func = window_func
		self.window_line, = self.ax_time.plot(ts, window_func(0))

		self.window_size = window_size
		# find the number of times each cycle needs to be repeated
		self.repeat_samples = int(np.ceil(len(ts) / window_size))

		self.frames = total_frames

	def repeat_sample(self, wave, offset):
		"""For a sample of the wave, repeat it for the entire range of ts"""
		sample = wave[offset:offset + self.window_size]
		full_wave = np.roll(np.tile(sample, self.repeat_samples), offset)[:len(self.ts)]
		return sample, full_wave


	def evaluate(self, i):
		"""Signal is to be evaluated for ts"""
		k = int((i / self.frames) * (len(self.ts) - self.window_size))

		window = self.window_func(k)

		windowed_wave = self.signal * window
		sample, full_wave = self.repeat_sample(windowed_wave, k)
		self.y_time = full_wave
		self.line_time.set_ydata(self.y_time)

		self.sampled_line.set_data(self.ts[k:self.window_size+k], sample)

		fft = np.fft.fft(self.y_time)
		N = len(self.ts)
		self.y_freq = 2. / N * np.abs(fft[0:N // 2])
		self.line_freq.set_ydata(self.y_freq)

		self.window_line.set_ydata(window)

		return [self.line_time, self.line_freq, self.window_line]


class SignalAnimator:
	"""Standalone class to plot movement of window across signal"""
	def __init__(self, ax, signal, ts, window_size, total_frames):
		self.ax = ax

		ax.set_xlim(ts[0], ts[-1])

		ax.plot(ts, signal, alpha=0.5, lw=2)

		self.signal = signal
		self.ts = ts
		self.frames = total_frames

		self.window_size = window_size
		self.time_size =  (self.window_size / len(signal)) * np.max(self.ts)
		self.window_line = ax.vlines([0, window_size/ts[-1]], -10, 10, color='tab:orange')
		self.sampled_line, = ax.plot([], [], color='tab:blue', lw=2)


	def evaluate(self, i):
		k = (i / self.frames) * (ts[-1] - self.time_size)
		line_data = [np.array([[k, -10], [k, 10]]),
					 np.array([[k+self.time_size, -10], [k+self.time_size, 10]]) ]
		self.window_line.set_segments(line_data)

		idx = int((i / self.frames) * (len(ts) - self.window_size))
		ts_sample = self.ts[idx:idx+self.window_size]
		ys_sample = self.signal[idx:idx+self.window_size]

		self.sampled_line.set_data(ts_sample, ys_sample)

		return [self.window_line]

	def init_func(self):
		return self.evaluate(0)

	def animate(self, i):
		return self.evaluate(i)

if __name__ == '__main__':
	signal_data = load_earthquake(3)
	rate = 500  # Hz
	signal = lambda: signal_data[:20000]

	ANIM_TIME = 10
	total_frames = int((ANIM_TIME * 1000) // INTERVAL)

	N = len(signal())
	T = 1 / rate
	ts = np.linspace(0, N / rate, N)
	fs =np.linspace(0., 1. / (2. * T), N // 2)

	# fig, ax = plt.subplots()
	# ax.plot(ts, signal())
	# ax.set_xlabel('time [s]')
	# plt.show()

	window_funcs = (hann, flat_top)
	window_names = ('Hann', 'flat top')
	anims = []
	window_size = 3000

	fig, all_axes = plt.subplots(nrows=3, ncols=2, sharey='row', figsize=(15, 10))

	# get big axis to plot signal
	gs = all_axes[0, 0].get_gridspec()
	for ax in all_axes[0, :]:
		ax.remove()

	axbig = fig.add_subplot(gs[0, :])

	signal_anim = SignalAnimator(axbig, signal(), ts, window_size, total_frames)

	anims = [signal_anim]
	window_axes = all_axes[1:, :]
	for ax_pair, window_func, window_name in zip(window_axes.T, window_funcs, window_names):
		window = get_window(window_size, window_func, len(ts))
		anim = EarthquakeAnimator(ax_pair, signal, ts, fs, window, window_size, total_frames,
								  log_amplitude=True)
		anims.append(anim)

		ax_pair[0].set_title(f'Window function: {window_name}')

	handles = (anim.line_freq, anim.window_line)
	fig.legend(handles, ('Signal', 'Sampled region'))

	grp = GroupAnimator(fig, anims, ANIM_TIME)
	grp.save('earthquake_window.gif', writer='ffmpeg')

	plt.show()