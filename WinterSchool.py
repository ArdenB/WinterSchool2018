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
import pandas as pd
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
	dates = ymonday(ncf1.variables["time"][:])
	
	# convert to a standard rater format way can use with imshow
	tmin2  = np.swapaxes(tmin1, 0, 2).astype(float)
	tmin3  = np.swapaxes(tmin2, 0, 1)

	# detrend the data
	from scipy import signal
	tmin_det = signal.detrend(tmin3, axis=2, type='linear')
	
	# calculate the extremes
	tmin = tmin_det.copy()

	tmin[tmin <xval] = 0
	tmin[tmin>=xval] = 1


	# test plot
	plt.imshow(np.sum(tmin, axis=2) )
	plt.colorbar()
	plt.show()

	# Print the max number
	print(np.max(np.sum(tmin, axis=2))) 
	ipdb.set_trace()

#==============================================================================
# def ymonday( dates ):
# 	y,m,d = [],[],[]
# 	for i in dates:
# 		y.append(int(i)/10000)
# 		m.append((i/100)%100)
# 		d.append(i%100)
# 	ipdb.set_trace()
# 	return y,m,d



if __name__ == '__main__':
	main()