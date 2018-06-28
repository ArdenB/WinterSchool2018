""" 
A class that can be used to store the key paramaters about the tested run 
"""
#==============================================================================

__title__ = "Mapping Class"
__author__ = "Arden Burrell"
__version__ = "1.1(18.02.2018)"
__email__ = "arden.burrell@gmail.com"

#==============================================================================
class mapclass(object):
	"""
	Class of object that contains infomation about the a map to be made.
	THis object is just a container to make it easier to make maps in the 
	MapMaker.py script 
		
	"""
	def __init__(self, region, pshow=True):
		# ========== the variables defined by the rundet ========== 

		# Useful infomation
		aus_names = ["AUS", "Australia"]

		# ===== Using the run infomation, determine the bounds for a map =====
		if region == "GLOBAL":
			self.region = "GLOBAL"
			self.bounds = [-180, 180, 90, -90]
		elif region in aus_names:
			self.region = "AUS"
			self.bounds = [112.0, 155.5, -43.5, -10]
		elif region == "MONG":
			self.region = "MONG"
			self.bounds = [85.0, 120.0, 52, 40]
		else:
			self.bounds = None
			import warnings 
			warnings.warn("The region code is unknown, unable to set bounds")
		
		self.pshow    = pshow # show the plot after saving?
		
		# ========== Set the blank variables ========== 
		self.plotpath = None
		self.var      = None # The variable being mapped
		self.cmap     = None # Colormap set later
		self.cmin     = None # the min of the colormap
		self.cmax     = None # the max of the colormap
		self.cZero    = None # the zero point of the colormap
		self.column   = None # the column to be mapped
		self.norm     = None
		self.ticks    = None # The ticks on the colorbar
		self.ticknm   = None # The tick names on the colorbar
		self.cbounds  = None
		self.mask     = None # used for passing drylands masks around
		
		# ========== Set the plot defualts ==========
		self.maskcol  = 'dimgrey'
		self.Oceancol = 'w'
		# Extend the colorbar to cover any data outside the cmap range
		self.extend   = "both" 
		self.spacing  = 'uniform'
		self.origin   = 'lower'
		


