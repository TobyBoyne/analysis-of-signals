"""Functions to process and analyse signals"""
import numpy as np
import matplotlib.pyplot as plt

from read_data import load_sweep

def transfer(ch1, ch2):
	f_1 = np.fft.fft(ch1)
	f_2 = np.fft.fft(ch2)

	return np.abs(f_2) / np.abs(f_1)


if __name__ == '__main__':
	ch1, ch2 = load_sweep(300)
	G = transfer(ch1, ch2)

	plt.plot(G[:len(G)//2])
	plt.show()