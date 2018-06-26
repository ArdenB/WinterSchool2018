""" Python script to perform the analysis """
#==============================================================================

__title__ = "Winter School 2018"
__author__ = "Arden Burrell"
__version__ = "v1.0(26.05.2018)"
__email__ = "arden.burrell@gmail.com"

#==============================================================================
# Import packages
import numpy as np
import scipy as sp
from scipy import stats
import pandas as pd
from numba import jit
import argparse
import datetime as dt
from collections import OrderedDict
import warnings as warn
from netCDF4 import Dataset, num2date 
# Import plotting and colorpackages
import matplotlib.pyplot as plt
# import matplotlib.colors as mpc
# import matplotlib as mpl
# import palettable 
# Import debugging packages 
import ipdb

#==============================================================================

def main():
	"""
	Script goal
		open the netcdf file
			process it to get a yearly score score for each pixel
		open the enso dataset
		regress the enso and netcdf files
	"""
	# ========== Get the temperature data ==========
	anuvals = NCopener(xval=24)

#==============================================================================
def NCopener(xval=24):
	"""
	Function opens the detrended NC file, then precesses it
	args:
		value  for extreme  threshold
	"""
	# set the file name
	# fn    = "./AWAP_sel_DJF.nc"
	fn 	  = "./AWAP_nondetrend_sel_DJF.nc"
	
	# load the data
	ncf1  = Dataset(fn, mode='r')
	# pull out the data
	tmin1 = np.asarray(ncf1.variables["tmin"][:])
	dates = time_split(ncf1.variables["time"][:])
	
	# convert to a standard rater format way can use with imshow
	tmin2  = np.swapaxes(tmin1, 0, 2).astype(float)
	tmin3  = np.swapaxes(tmin2, 0, 1)

	# calculate a mean annual temperature and detrend
	from scipy import signal
	tmin_det = signal.detrend(tmin3, axis=2)

	# work out a date is in the referenc period 
	yvals = range(1911, 1942)
	ref = []
	for vls in dates:
		ref.append(vls in yvals)

	refmean = np.mean(tmin3[:, :, ref], axis=2)
	rfm = np.repeat(refmean[:, :, np.newaxis], tmin_det.shape[2], axis=2)
	
	# calculate the extremes
	tmin = rfm + tmin_det

	tmin[tmin <xval] = 0
	tmin[tmin>=xval] = 1





	# Get an annual score
	stack = []
	years = range(1911, 2014)
	for year in years:
		# calculate the true fales array
		ref = []
		for dt in dates:
			ref.append(dt == year)

		stack.append(np.sum(tmin[:,:,ref], axis=2))
	# stack the annual counds
	xccount = np.dstack(stack)
	# test plot

	# load the enso data
	enso =  np.asarray(pd.read_csv("./best.csv")).reshape(-1) 

	#  perform the regression
	print("Starting the regressions")
	coef = threeDloop(xccount, enso)
	plt.imshow(coef[:, :, 0])
	plt.colorbar()
	plt.show()

	ipdb.set_trace()

#==============================================================================
def time_split(t):
	y,m,d = [],[],[]
	for i in t:
		y.append(int(i)/10000)
		m.append((i/100)%100)	
	for j in range(len(m)):
		if m[j] == 1 or m[j] == 2:
			y[j] = y[j]-1
	a = y[0]
	for i in range(len(y)):
		if y[i] == a:
			y[i] = 0
		if y[i] == y[-1]:
			y[i] = 0
	# print(y)
   	return y

@jit
def threeDloop(xccount, enso):

	coef = np.zeros((xccount.shape[0], xccount.shape[1], 5))
	# loop ove the y and x dim
	for y in range(0, xccount.shape[0]):
		for x in range(0, xccount.shape[1]):
			coef[y, x, :] = scipyols(xccount[y, x, :], enso)
	return coef

@jit
def scipyols(array, enso):
	"""
	Function for rapid OLS with time. the regression is done with 
	an independent variable rangeing from 0 to array.shape to make
	the intercept the start which simplifies calculation
	args:
		array 		np : numpy array of annual max VI over time 
	return
		result 		np : change(total change between start and end)
						 slope, intercept, rsquared, pvalue, std_error
	"""
	# +++++ Get the OLS +++++
	slope, intercept, r_value, p_value, std_err = stats.linregress(
		np.arange(array.shape[0]), array)
	# +++++ calculate the total change +++++
	# +++++ return the results +++++
	return np.array([slope, intercept, r_value**2, p_value, std_err])


if __name__ == '__main__':
	main()