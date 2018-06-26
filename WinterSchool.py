""" Python script to perform the analysis """
#==============================================================================

__title__ = "Winter School 2018"
__author__ = "Arden Burrell"
__version__ = "v1.0(26.05.2018)"
__email__ = "arden.burrell@gmail.com"

#==============================================================================
# Import packages
import numpy as np
import pandas as pd
import argparse
import datetime as dt
from collections import OrderedDict
import warnings as warn
from netCDF4 import Dataset, num2date 
# Import plotting and colorpackages
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib as mpl
import palettable 
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
	 fn = "./AWAP_sel_DJF.nc "

	 # load the data
	 ncf1 = Dataset(fn, mode='r')

	 tmin = ncf1.variables["tmin"][:]
	 ipdb.set_trace()


#==============================================================================

if __name__ == '__main__':
	main()