import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from window.window_funcs import rectangular

INTERVAL = 30

class GroupAnimator(FuncAnimation):
	"""Stores multiple Animator objects
	Allows for side-by-side rendering"""
	def __init__(self, fig, anims, T):
		self.anims = anims
		total_frames = int((T * 1000) // INTERVAL)
		kwargs = {
			"init_func": self.init_func,
			"frames": total_frames,
			"interval": INTERVAL,
			"blit": False
		}

		super().__init__(fig, self.animate, **kwargs)

	def init_func(self):
		anim_data = []
		for anim in self.anims:
			anim_data += anim.init_func()
		return anim_data

	def animate(self, i):
		anim_data = []
		for anim in self.anims:
			anim_data += anim.animate(i)
		return anim_data


class Animator:
	"""Object stores all signals to be animated
	Contains time domain and frequency domain plots
	Main drawing stored in self.line
	init() is called at the beginning of each loop
	animate() is called at each frame"""
	def __init__(self, axes, window_func, signal_func, ts, fs, **kwargs):
		self.ax_time, self.ax_freq = axes


		self.ax_time.set_xlabel('time [s]')
		self.ax_freq.set_xlabel('frequency [Hz]')

		self.window = window_func(ts) if window_func is not None else rectangular(ts)
		self.signal = signal_func


		if kwargs.get('plot_markers', False):
			self.line_time, = self.ax_time.plot(ts, np.zeros_like(ts), lw=3,
												marker='x', markersize=10, markeredgewidth=3, markeredgecolor='tab:cyan')
		else:
			self.line_time, = self.ax_time.plot(ts, np.zeros_like(ts), lw=3)

		if kwargs.get('log_amplitude', False):
			self.line_freq, = self.ax_freq.semilogy(fs, np.zeros_like(fs), lw=3)
		else:
			self.line_freq, = self.ax_freq.plot(fs, np.zeros_like(fs), lw=3)

		self.ts = ts
		self.fs = fs
		self.y_time = []
		self.y_freq = []

		# plot window function on time axis
		# if kwargs.get('plot_window', False):


	def evaluate(self, k):
		"""Base animator class has no evalution method"""
		return [self.line_time, self.line_freq]


	def init_func(self):
		return self.evaluate(0)

	def animate(self, i):
		return self.evaluate(i)


if __name__ == '__main__':
	from window.window_funcs import *
	from sampling.sample_rate_plot import SampleRateAnimator
	fig, axes = plt.subplots(nrows=2)

	N = 1000
	total_time = 20.
	T = total_time / N

	ts = np.linspace(0., total_time, N)
	fs = np.linspace(0., 1. / (2. * T), N // 2)


	window_func = flat_top

	signal = lambda k: np.sin(2*np.pi*k*ts / 4)
	# anim = Animator(axes, window_func, signal, ts, fs)
	# group_anim = GroupAnimator(fig, [anim], 3)

	signal = lambda t: np.sin(2*np.pi*t*2)
	anim = SampleRateAnimator(axes, signal, 2, fs)
	group_anim = GroupAnimator(fig, [anim], 3)

	plt.show()