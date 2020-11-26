import numpy as np
import matplotlib.pyplot as plt

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
	N = 300
	total_time = 20.
	T = total_time / N

	x = np.linspace(0., N*T, N)
	xf = np.linspace(0., 1./(2.*T), N//2)

	sig = np.sin(1.5 * 2.*np.pi*x)

	yf = dft(sig)
	yf_fast = np.fft.fft(sig)

	ax_sig.plot(x, sig)
	ax_fourier.plot(xf, 2./N * np.abs(yf_fast[0:N//2]))
	ax_fourier.plot(xf, 2./N * np.abs(yf[0:N//2]))

	plt.show()
