"""Implementation of a Discrete Fourier Transform with time comparison"""

import numpy as np
import matplotlib.pyplot as plt
from timeit import timeit

def dft(signal):
	"""Perform a discrete fourier transform on an input signal"""

	N = len(signal)
	n = np.arange(0, N, 1, dtype=float)

	n = n[:, np.newaxis]
	k_n_mat = n @ n.T
	X = np.sum(signal * np.exp(-2j * np.pi * k_n_mat / N), axis=-1)
	return X


if __name__ == '__main__':
	fig, (ax_sig, ax_fourier) = plt.subplots(nrows=2)
	N = 1000
	total_time = 20.
	T = total_time / N

	x = np.linspace(0., N*T, N)
	xf = np.linspace(0., 1./(2.*T), N//2)

	sig = np.sin(1.5 * 2.*np.pi*x) + 2*np.sin(3. * 2.*np.pi*x)

	yf = dft(sig)
	yf_fast = np.fft.fft(sig)

	# time test
	n_repeats = 20
	t_dft = timeit(lambda: dft(sig), number=n_repeats) / n_repeats
	t_fast = timeit(lambda: np.fft.fft(sig), number=n_repeats) / n_repeats
	print(f'DFT time taken: {t_dft * 1e3:.4f} ms')
	print(f'FFT time taken: {t_fast * 1e3:.4f} ms')

	ax_sig.plot(x, sig)
	ax_fourier.plot(xf, 2./N * np.abs(yf_fast[0:N//2]))
	ax_fourier.plot(xf, 2./N * np.abs(yf[0:N//2]))

	plt.show()
