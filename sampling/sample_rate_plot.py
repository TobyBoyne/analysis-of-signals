import numpy as np
import matplotlib.pyplot as plt

from animate import GroupAnimator, Animator, INTERVAL


class SampleRateAnimator(Animator):
	def __init__(self, axes, signal_func, t_max, fs, **kwargs):
		ts = np.linspace(0, t_max, 1)
		super().__init__(axes, None, signal_func, ts, fs, **kwargs)
		self.t_max = t_max

		self.ax_time.set_xlim(0, t_max)
		self.ax_time.set_ylim(-1, 1)

		self.ax_freq.set_xlim(0, 10)
		self.ax_freq.set_ylim(0, 1.5)

		# plot for large sample rate
		ts_final = np.linspace(0, t_max, 1000)
		N = len(ts_final)
		T = self.t_max / N
		fs_final = np.linspace(0., 1. / (2. * T), N // 2)

		ys_final = signal_func(ts_final)
		fft_final = np.fft.fft(ys_final)
		y_freq_final = 2. / N * np.abs(fft_final[0:N // 2])

		self.ax_time.plot(ts_final, ys_final, linestyle='--')
		self.ax_freq.plot(fs_final, y_freq_final, linestyle='--')


	def evaluate(self, i):
		"""Signal is to be evaluated for ts"""
		k = int(np.exp(i / 40) + 1)
		self.ax_time.set_title(f'Number of sampled points = {k}')
		self.ts = np.linspace(0, self.t_max, int(k))
		N = len(self.ts)
		T = self.t_max / N
		self.fs = np.linspace(0., 1. / (2. * T), N // 2)


		self.y_time = self.signal(self.ts)
		self.line_time.set_data(self.ts, self.y_time)

		fft = np.fft.fft(self.y_time)
		self.y_freq = 2. / N * np.abs(fft[0:N // 2])
		self.line_freq.set_data(self.fs, self.y_freq)

		return [self.line_time, self.line_freq]


if __name__ == '__main__':
	from window.window_funcs import rectangular
	fig, axes = plt.subplots(nrows=2, figsize=(10, 15))

	N = 1000
	total_time = 20.
	T = total_time / N

	fs = np.linspace(0., 1. / (2. * T), N // 2)


	signal = lambda t: np.sin(2 * np.pi * t * 4.10)
	anim = SampleRateAnimator(axes, signal, 2, fs,
							  plot_markers=True)
	grp = GroupAnimator(fig, [anim], 7)
	# grp.save('rate_sine_sweep.gif', writer='ffmpeg')
	# grp.save('rate_4100mHz.gif', writer='ffmpeg')
	plt.show()