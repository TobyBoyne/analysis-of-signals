#https://en.wikipedia.org/wiki/Window_function#Hann_and_Hamming_windows

import numpy as np
import matplotlib.pyplot as plt

def rectangular(n):
	return 1

def triangular(n):
	return 1 - np.abs((2*n - len(n)) / (len(n)+1))

def hamming(n, a=0.2):
	return a - (1 - a) * np.cos(2 * np.pi * n / len(n))

def hann(n):
	return hamming(n, 0.5)

def flat_top(n):
	a = np.array([0.215, -0.417, 0.277, -0.0836, 0.006947])
	c = np.arange(0, 10, 2).reshape(1, -1)
	n = n.reshape(-1, 1)

	return np.sum(a * np.cos((n @ c) * np.pi / len(n)), axis=-1)

if __name__ == '__main__':
	n = np.arange(1, 100)
	window = hann(n)
	window2 = triangular(n)
	print(window2)

	plt.plot(window)
	plt.plot(window2)
	plt.show()
