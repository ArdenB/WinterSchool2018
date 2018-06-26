# -*- coding: utf-8 -*-
"""
Function to make maps


"""
#==============================================================================

__title__ = "Map Maker"
__author__ = "Arden Burrell"
__version__ = "1.3(18.03.2018)"
__email__ = "arden.burrell@gmail.com"

#==============================================================================

# Import packages
import numpy as np
import pandas as pd
import sys	
import ipdb
# import datetime as dt

# Mapping packages
import cartopy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cpf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

import matplotlib.pyplot as plt
# from  .. import CoreFunctions as cf 	

#==============================================================================

#==============================================================================
def mapmaker(image, mapdet):
	"""Function to Build some maps"""
	# ========== Check the class of the input data ==========
	# if type(mapdet).__name__ != 'mapclass':
		# raise TypeError("mapdet must be of class mapclass")

	# =========== convert the QRB to an SQRB image  ===========
	# if not (mapdet.mask is None):
		# image *= mapdet.mask

	plt.rcParams.update({'figure.subplot.right' : 0.85 })
	plt.rcParams.update({'figure.subplot.left' : 0.05 })

	fig, ax = plt.subplots(1, 1, figsize=(18,9),
		subplot_kw={'projection': ccrs.PlateCarree()}, 
		num=("Map of %s" % mapdet.var))
	
	# re-calculated at each figure resize. 
	cbar_ax = fig.add_axes([0, 0, 0.1, 0.1])


	# ========== plot the image ==========
	# pdb.set_trace()
	im = ax.imshow(image, 
		extent=mapdet.bounds, 
		cmap=mapdet.cmap, 
		norm=mapdet.norm, 
		origin='lower',
		) # added after australia looked lame



	# ========== Add features to the map ==========
	ax.add_feature(cpf.OCEAN, facecolor="w")
	ax.add_feature(cpf.COASTLINE)	
	ax.add_feature(cpf.BORDERS, linestyle='--')
	ax.add_feature(cpf.LAKES, alpha=0.5)
	ax.add_feature(cpf.RIVERS)
	# ax.gridlines()



	# =========== Set up the axis ==========
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, 
		linestyle='--')

	gl.xlocator = mticker.FixedLocator(range(110, 170, 10))
	gl.ylocator = mticker.FixedLocator(range(-10, -55, -10))

	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	
	# ========== Add an autoressining colorbar ========== 
	def resize_colobar(event):
		plt.draw()

		posn = ax.get_position()
		cbar_ax.set_position([posn.x0 + posn.width + 0.03, posn.y0, 0.025, posn.height])

	fig.canvas.mpl_connect('resize_event', resize_colobar)

	# ax.coastlines()
	# set the limits on the colorbar
	im.set_clim(mapdet.cmin, mapdet.cmax)
	# set the position of the colorbar
	posn = ax.get_position()
	cbar_ax.set_position(
		[posn.x0 + posn.width + 0.03, posn.y0, 0.025, posn.height]
		)


	cb = plt.colorbar(
		im, 
		cax        = cbar_ax, 
		extend     = mapdet.extend, 
		norm       = mapdet.norm,
		ticks      = mapdet.ticks, 
		spacing    = mapdet.spacing,
		boundaries = mapdet.cbounds # [-1] + mapdet.cbounds + [1]
		)

	# if not (mapdet.ticknm is None):
	# 	cb.ax.set_yticklabels(mapdet.ticknm) 

	# # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
	# # ========== save the plot ==========
	# if not (mapdet.plotpath is None):
	# 	# Make a pdf version
	# 	fnm_pdf = "%s%d._map_%s.pdf" % (
	# 		mapdet.plotpath, (mapdet.column), mapdet.var)
	# 	plt.savefig(fnm_pdf)
			
	# 	# make png version 
	# 	fname = "%s%d._BasicFigs_%s.png" % (
	# 		mapdet.plotpath, (mapdet.column), mapdet.var)
	# 	plt.savefig(fname)
	# 	plotinfo = "PLOT INFO: Plot of %s made using %s:v.%s" % (
	# 		mapdet.var, __title__, __version__)
	# else:
	# 	fname = None
	# if mapdet.pshow:
	plt.show()
	plt.close()
	# Reset the the plt paramters to the defualts
	plt.rcParams.update(plt.rcParamsDefault)
	# return the infomation
	# return plotinfo, fname

