#https://en.wikipedia.org/wiki/Window_function#Hann_and_Hamming_windows
#https://en.wikipedia.org/wiki/Window_function#Discrete-time_signals

import numpy as np
import matplotlib.pyplot as plt

def rectangular(n):
	return np.ones_like(n)

def triangular(n):
	N = np.max(n)
	return 1 - np.abs((2*n - N) / (N+1))

def hamming(n, a=0.2):
	N = np.max(n)
	return a - (1 - a) * np.cos(2 * np.pi * n / N)

def hann(n):
	return hamming(n, 0.5)

def flat_top(n):
	N = np.max(n)
	a = np.array([0.215, -0.417, 0.277, -0.0836, 0.006947])
	c = np.arange(0, 10, 2).reshape(1, -1)
	n = n.reshape(-1, 1)

	return np.sum(a * np.cos((n @ c) * np.pi / N), axis=-1)

if __name__ == '__main__':
	n = np.arange(1, 100)
	t = (2 * np.pi / 50) * n
	signal = np.sin(t) + 0.5 * np.sin(2*t)+ 0.2 * np.sin(4*t)
	plt.plot(signal)

	fig, axes = plt.subplots(2, 2)

	for ax, window_func in zip(axes.flat, (rectangular, triangular, hann, flat_top)):
		ax.plot(window_func(n))
		ax.plot(signal * window_func(n))
		ax.grid()

	plt.show()
