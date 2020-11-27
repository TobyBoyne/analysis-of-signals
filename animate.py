import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

INTERVAL = 20

class GroupAnimator(FuncAnimation):
	"""Stores multiple Animator objects
	Allows for side-by-side rendering"""
	def __init__(self, fig, anims, T):
		self.anims = anims
		total_frames = int(T * 1000 // INTERVAL)
		kwargs = {
			"init_func": self.init_func,
			"frames": total_frames,
			"interval": INTERVAL,
			"blit": True
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
	Arrows of coefficients stored in self.arrows
	init() is called at the beginning of each loop
	animate() is called at each frame"""
	def __init__(self, ax, fourier):
		# init function for FuncAnimation
		self.line, = ax.plot([], [], lw=3)
		self.x_data = []
		self.y_data = []

	def init_func(self):
		self.x_data = []
		self.y_data = []
		self.line.set_data([], [])
		return [self.line,]

	def animate(self, i):
		t = i * (INTERVAL / 1000)

		self.line.set_data(self.x_data, self.y_data)

		return [self.line,]