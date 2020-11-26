"""Functions for loading matlab .mat files"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as spio

def load_data(fname):
	mat = spio.loadmat(f'experimental_data/{fname}.mat', squeeze_me=True)
	arr_ch1 = mat['data_ch1']
	arr_ch2 = mat['data_ch2']
	return arr_ch1, arr_ch2

def load_sine(fs, channel='A1'):
	"""Load a sine wave, where fs are the frequencies and channel
	is the output channel used"""
	fname = f'sine{fs}_F0{channel}_300Hz'
	return load_data(fname)

def load_sweep(f, channel='A1'):
	"""Load a sweep, where f is the frequency of the driving force"""
	if type(f) != 'str': f = str(int(f))
	fname = f'sweep1to20_F0{channel}_{f}Hz'
	return load_data(fname)

def load_random(channel='A1'):
	"""Load the random data"""
	fname = f'random_20timesLarger_F0{channel}_300Hz'
	return load_data(fname)

if __name__ == '__main__':
	ch1, ch2 = load_random('A1')
	ch1, ch2 = load_sweep(300)

	plt.plot(ch1[:100])
	plt.plot(ch2[:100])
	plt.show()