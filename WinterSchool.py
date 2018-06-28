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
import matplotlib.colors as mpc
import matplotlib as mpl
import palettable 
import statsmodels.formula.api as smf
import Modules.PlotFunctions as pf
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
def NCopener(xval=29):
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
	# make a 3d array containing the mean correction
	rfm = np.repeat(refmean[:, :, np.newaxis], tmin_det.shape[2], axis=2)
	
	# calculate the extremes
	tmin = rfm + tmin_det
	tmin[tmin <xval] = 0
	tmin[tmin>=xval] = 1


	# Get the number of extreme events in each year
	stack = []
	years = range(1911, 2014)
	for year in years:
		# calculate the true fales array
		ref = []
		for dt in dates:
			ref.append(dt == year)
		stack.append(np.sum(tmin[:,:,ref], axis=2))
	# stack the annual counds of extere values
	xccount = np.dstack(stack)
	count_map(xccount)

	#  perform the regression
	print("Starting the regressions")
	
	# load the enso data
	enso =  np.asarray(pd.read_csv("./best.csv")).reshape(-1) 
	IOD  =  np.asarray(pd.read_csv("./dmi_std.csv")).reshape(-1) 

	# get the regression coeficents (slope, intercept, r2, pvalue, std error)
	coef = threeDloop(xccount, enso)
	ipdb.set_trace()
	# mask p>0.05 (non significant)
	slope = coef[:, :, 0] 
	inter = coef[:, :, 1] #intercept
	pval  = coef[:, :, 3] 
	slope[pval>0.05] = np.NAN 
	inter[pval>0.05] = np.NAN 
	np.save("./regression_coef_ENSO.npy", coef)

	# make a map
	mapper(coef, "ENSO (NINO 3.4)")
	coef = None 

	# load the enso data
	
	# get the regression coeficents (slope, intercept, r2, pvalue, std error)
	coef = threeDloop(xccount, IOD)

	# mask p>0.05 (non significant)
	slope = coef[:, :, 0] 
	inter = coef[:, :, 1] #intercept
	pval  = coef[:, :, 3] 
	slope[pval>0.05] = np.NAN 
	inter[pval>0.05] = np.NAN 
	np.save("./regression_coef_IOD.npy", coef)
	# make a map
	mapper(coef, "IOD (DMI)")

	coef = None 
	coef = threeDloop(xccount, enso, IOD)

	# mask p>0.05 (non significant)
	slope = coef[:, :, 0] 
	inter = coef[:, :, 1] #intercept
	pval  = coef[:, :, 3] 
	slope[pval>0.05] = np.NAN 
	inter[pval>0.05] = np.NAN 
	np.save("./regression_coef_IODandENso.npy", coef)
	mapper(coef, "ENSOandIOD")




#==============================================================================
def count_map(xccount):

	xmean = np.nanmean(xccount, axis=2)

	mapdet = pf.mapclass(region="AUS")
	# pick a colormap
	# cmap = mpc.ListedColormap(palettable.colorbrewer.diverging.RdBu_8_r.mpl_colors)
	cmap   = plt.cm.viridis
	# set the min and max for the colormap
	mapdet.cmin =   0
	mapdet.cmax =   90
	mapdet.origin = "upper"
	mapdet.extend = "neither"

	# set thee title
	mapdet.var  = "HotNights"
	pf.mapmaker(xmean, mapdet)



	pass

def mapper(coef, varmode):

	"""Takes the recression coeficents and makes maps of them"""
	
	# =========== slope ===========
 	print("Map of the slope Hot Nigths vs %s " % varmode)
	
	# build an object to hold the metadata
	# 	Cheat by using a class i built, 
	#    its just a container for infomation for the plot
	mapdet = pf.mapclass(region="AUS")
	# pick a colormap
	cmap = mpc.ListedColormap(palettable.colorbrewer.diverging.RdBu_8_r.mpl_colors)
	cmap.set_bad(mapdet.maskcol)
	mapdet.cmap = cmap
	# set the min and max for the colormap
	mapdet.cmin =  -8.0
	mapdet.cmax =   8.0

	# set thee title
	mapdet.var  = "HotNightsvs%s_Slope" %  varmode
	pf.mapmaker(coef[:, :, 0], mapdet)
	
	# =========== R2 ===========
 	print("Map of the r2")
	
	# build an object to hold the metadata
	# pick a colormap
	cmap = mpc.ListedColormap(palettable.matplotlib.Magma_8.mpl_colors)
	cmap.set_bad(mapdet.maskcol)
	mapdet.cmap = cmap
	# set the min and max for the colormap
	mapdet.cmin   = 0
	mapdet.cmax   = 0.2
	mapdet.extend = "max"
	# set thee title
	mapdet.var    = "HotNightsvs%s_R2" %  varmode
	pf.mapmaker(coef[:, :, 2], mapdet)
	
	# =========== p values ===========
 	print("Map of the p values")
	
	# build an object to hold the metadata
	# pick a colormap
	cmap = mpc.ListedColormap(palettable.matplotlib.Viridis_10.mpl_colors)
	cmap.set_bad(mapdet.maskcol)
	mapdet.cmap   = cmap
	# set the min and max for the colormap
	mapdet.cmin   = 0
	mapdet.cmax   = 0.5
	mapdet.extend = "max"
	# set thee title
	mapdet.var    = "HotNightsvs%s_pvalues" %  varmode
	pf.mapmaker(coef[:, :, 3], mapdet)

def time_split(t):
	"""
	Function takes the dates from the netcdf and works out which 
	year values belong too
	"""
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
def threeDloop(xccount, index, other=None):

	coef = np.zeros((xccount.shape[0], xccount.shape[1], 5))
	# loop ove the y and x dim
	for y in range(0, xccount.shape[0]):
		for x in range(0, xccount.shape[1]):
			if other is None:
				coef[y, x, :] = scipyols(xccount[y, x, :], index)
			else:
				df = pd.DataFrame({"nights":xccount[y, x, :], "enso":index, "IOD":other})
				coef[y, x, :] = MV_OLS(df)
	return coef

@jit
def scipyols(array, index):
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
	slope, intercept, r_value, p_value, std_err = stats.linregress(index, array)
	# +++++ calculate the total change +++++
	# +++++ return the results +++++
	return np.array([slope, intercept, r_value**2, p_value, std_err])

def MV_OLS(df):
	"""
	Function for rapid OLS with time. the regression is done with 
	an independent variable rangeing from 0 to array.shape to make
	the intercept the start which simplifies calculation
	args:
		array 		np : numpy array of annual max VI over time 
		dummy 		np : numpy array containg the breakpoint variable
	return
		result 		np : change(total change between start and end)
	"""
			
	# ========== Fit the regression ============
	mod = smf.ols(formula = 'nights~enso*IOD', data=df).fit()
	# ===== Pull out key values =====
	# change   = mod.fittedvalues[33] - mod.fittedvalues[0] - bh
	r2_value = mod.rsquared_adj
	p_value  = mod.f_pvalue
	return np.array([np.NAN, np.NAN, r2_value, p_value, np.NAN])
if __name__ == '__main__':
	main()