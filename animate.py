import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
	Main drawing stored in self.line
	init() is called at the beginning of each loop
	animate() is called at each frame"""
	def __init__(self, axes, window_func, signal_func, ts, fs):
		self.ax_time, self.ax_freq = axes

		self.ax_time.set_xlim(0, np.max(ts))
		self.ax_time.set_ylim(-1, 1)
		self.ax_time.set_xlabel('time [s]')

		self.ax_freq.set_xlim(0, 2)
		self.ax_freq.set_ylim(0, 1.5)
		self.ax_freq.set_xlabel('frequency [Hz]')

		self.window = window_func(ts)
		self.signal = signal_func

		self.line_time, = self.ax_time.plot(ts, np.zeros_like(ts), lw=3)
		self.line_freq, = self.ax_freq.plot(fs, np.zeros_like(fs), lw=3)

		self.ts = ts
		self.fs = fs
		self.y_time = []
		self.y_freq = []

		# plot window function on time axis
		self.ax_time.plot(ts, self.window)

	def evaluate(self, k):
		N = len(self.ts)

		self.y_time = self.signal(k) * self.window
		self.line_time.set_ydata(self.y_time)

		fft = np.fft.fft(self.y_time)
		self.y_freq = 2. / N * np.abs(fft[0:N // 2])
		self.line_freq.set_ydata(self.y_freq)

		return [self.line_time, self.line_freq]


	def init_func(self):
		return self.evaluate(0)

	def animate(self, i):
		k = i * (INTERVAL / 1000)
		return self.evaluate(k)

if __name__ == '__main__':
	from window.window_funcs import triangular
	fig, axes = plt.subplots(nrows=2)

	N = 1000
	total_time = 20.
	T = total_time / N

	ts = np.linspace(0., total_time, N)
	fs = np.linspace(0., 1. / (2. * T), N // 2)


	window_func = triangular(ts)

	signal = lambda k: np.sin(2*np.pi*k*ts / 4)
	anim = Animator(axes, window_func, signal, ts, fs)
	group_anim = GroupAnimator(fig, [anim], 3)
	plt.show()