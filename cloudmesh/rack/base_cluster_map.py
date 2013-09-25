"""
Base class for different .diag render with rackdiag
"""

from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.util.util import path_expand as cm_path_expand

from jinja2 import Template
from hostlist import expand_hostlist
from sh import rackdiag  # @UnresolvedImport
from sh import rm  # @UnresolvedImport
from sh import pwd  # @UnresolvedImport
from sh import mkdir # @UnresolvedImport
import random
import time
import colorsys
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.lines import Line2D
import matplotlib.patches as patches


class BaseClusterMap:
	# default location of yaml configuration file
	default_home_yaml = "~/.futuregrid"
	
	# default location of cloudmesh_clusters.yaml
	default_clusters_yaml = "cloudmesh_cluster.yaml"

	# default location of cloudmesh_rack.yaml
	default_rack_yaml = "cloudmesh_rack.yaml"

	# the name of Clusters
	cluster_name_all = "all"
	cluster_name_unknown = "unknown"
	cluster_name = cluster_name_unknown

	# cluster name list in rack yaml configuration
	# default element only one element, "all", means including all other clustes
	cluster_name_list = [ cluster_name_all ]

	# clusters config parsed from default_clusters_yaml file
	dict_clusters_config = None

	#
	# servers dict
	# this will be used to render the original .diag file with Template
	# sub-class must fill this field with its specific characteristics
	# for example, a heat map dict:
	# 	 formation: {('i001', '[color="#FF0000"]'), (..., ...) ...}
	#
	dict_servers = {}

	#
	# cluster rack configuration dict
	# the global routine is: cloudmesh:rack:cluster
	# its children are: all, bravo, delta, echo, india and unknown
	dict_rack_config = None
	
	#
	# type of image with rackdiag
	#
	# If more image type supported, append the list to ["svg", "png", "gif", "jpg", ...]
	image_type_list = ["svg", "png"]
	
	# subclass type list
	subclass_type_list = ["temperature", "service"]
	
	# user choose a specific image type from image_type_list,
	# if not, the default type will be the default_image_type, "svg"
	image_type = ""
	
	# subclass type
	subclass_type = ""

	#
	# filename of rack image generated by rackdiag
	#
	only_filename_image = ""
	only_filename_legend = ""
	filename_rack_image = ""
	filename_rack_legend = ""

	# filename of .diag
	# get this filename by reading configuration of default_rack_yaml
	filename_diag = ""

	# temporary diag file, generated by Template render from filename_diag
	# this file will be used as a source file to generate a rack image with rackdiag
	# btw, this file can be deleted after use according to the flag_delete_temp_diag
	filename_diag_temp = ""

	#
	# flag of delete filename_diag_temp after used
	#
	flag_delete_diag_temp = True

	#
	# flag of DEBUG used ONLY
	# we use random generated data instead of the real data reading from clusters
	#
	flag_debug = True


	# construction function with default and image type rack filename
	def __init__(self, name, subclass_type=None, dir_yaml=None, dir_diag=None, dir_output=None, img_type=None):
		# init params with default values
		if subclass_type is None:
			subclass_type = self.subclass_type_list[0]
		if dir_yaml is None:
			dir_yaml = self.guessDefaultConfigLocation()
		if dir_diag is None:
			dir_diag = self.guessDefaultDiagLocation()
		if dir_output is None:
			dir_output = self.guessDefaultDiagramLocation()
		if img_type is None:
			img_type = self.image_type_list[0]
		
		abs_dir_yaml = cm_path_expand(dir_yaml)
		abs_dir_diag = cm_path_expand(dir_diag)
		abs_dir_output = cm_path_expand(dir_output)
		
		print "dir output,,,,,", abs_dir_output
		# make sure the output directory exist
		mkdir("-p", abs_dir_output)
		
		self.readClustersConfig(abs_dir_yaml)
		self.readRackConfig(name, abs_dir_yaml, abs_dir_diag)
		self.setRackImageType(subclass_type, img_type, abs_dir_output)
		self.initDictServers()


	# ======================================
	#		   abstract function
	#		 sub-class MUST override
	# ======================================
	#
	# get default value for dict_servers
	def getServersDefaultValue(self):
		pass


	# ======================================
	#		   abstract function
	#		 sub-class MUST override
	# ======================================
	#
	# get corresponding mapping dict, from specific value to RGB value
	# the formation of RGB is: (R, G, B)
	# for example: {1:(255, 0, 16), 2:(25, 20, 16), ...}
	def getMappingDict(self):
		pass


	# ======================================
	#		   abstract function
	#		 sub-class MUST override
	# ======================================
	#
	# get the current status of servers
	# params: dict_values means the data get from each server
	# this function MUST be called before plot to refresh status of servers in memory
	def update(self, dict_values):
		pass


	# ======================================
	#		   abstract function
	#		 sub-class MUST override
	# ======================================
	#
	# plot the legend of cluster map
	# param, ax is an instance of matplotlib.axes.Axes
	# return value is the filename of legend image file
	def drawLegendContent(self, ax, xylim):
		pass


	# read clusters config
	def readClustersConfig(self, dir_yaml):
		clusters_config = ConfigDict(filename=dir_yaml + "/" + self.default_clusters_yaml)
		self.dict_clusters_config = clusters_config["clusters"]
		# get all possible cluster names from dict_clusters_config
		self.cluster_name_list += self.dict_clusters_config.keys()

		print "clusters name list: ", self.cluster_name_list


	# read default_rack_yaml configuration
	def readRackConfig(self, name, dir_yaml, dir_diag):
		rack_config = ConfigDict(filename=dir_yaml + "/" + self.default_rack_yaml)
		self.dict_rack_config = rack_config["cloudmesh"]["rack"]
		print self.dict_rack_config

		lname = name.lower()
		self.cluster_name = lname if lname in self.cluster_name_list else self.cluster_name_unknown
		print "rack name is: ", self.cluster_name
		
		# diag filename
		self.filename_diag = dir_diag + "/" + self.dict_rack_config["cluster"][self.cluster_name]
		self.filename_diag_temp = self.filename_diag + ".temp"


	# set the type of rack image
	def setRackImageType(self, subclass_type, img_type, dir_output):
		ltype = subclass_type.lower()
		self.subclass_type = ltype if ltype in self.subclass_type_list else self.subclass_type_list[0]
		
		# lower string of type
		ltype = img_type.lower()

		if ltype in self.image_type_list:
			self.image_type = ltype
		else:
			print "[Warn]BaseClusterMap: Rack image type {0} is NOT supported currently!\n Use {1} to replace.".format(img_type, self.image_type_list[0])
			self.image_type = self.image_type_list[0]

		# filename, diag filename ends with ".diag"
		# image filename ends with "." + a valid lower image type
		image_basename = self.cluster_name + "-" + self.subclass_type;
		self.only_filename_image = image_basename + "." + self.image_type
		self.only_filename_legend = image_basename + "-legend.png"
		self.filename_rack_image = dir_output + "/" + self.only_filename_image
		self.filename_rack_legend = dir_output + "/" + self.only_filename_legend
		

		print "rack image filename is: ", self.filename_rack_image


	# initialize dict servers
	# formation, {"i001":None, "i002":None, ...}
	def initDictServers(self):
		if self.cluster_name == self.cluster_name_unknown:
			return

		servers_range_list = []
		print "rack name is: ", self.cluster_name
		if self.cluster_name == self.cluster_name_all:
			for name in self.dict_clusters_config.keys():
				print "clusters config name.id: ", self.dict_clusters_config[name]["id"]
				servers_range_list.append(self.dict_clusters_config[name]["id"])
		else:
			servers_range_list.append(self.dict_clusters_config[self.cluster_name]["id"])

		# server name list, add more server here
		list_servers = []
		for spec in servers_range_list:
			servers = expand_hostlist(spec)
			list_servers += servers
			
		self.dict_servers = dict.fromkeys(list_servers, self.getServersDefaultValue())


	# 
	# reset dict servers to a default value
	#
	def resetDictServers(self, value):
		for server in self.dict_servers:
			self.dict_servers.update({server:value})
		pass


	# update a server info in dict servers
	def updateServer(self, server, value):
		self.dict_servers.update({server:value})
	
	
	#
	# Enable/Disable the function of delete filename_diag_temp after used
	#
	def enableDeleteDiagTemp(self):
		self.flag_delete_diag_temp = True

	def disableDeleteDiagTemp(self):
		self.flag_delete_diag_temp = False


	# only filename
	def getImageFilename(self):
		return self.only_filename_image
	
	def getLegendFilename(self):
		return self.only_filename_legend

	# render dict_servers with correct colors
	# param: mapping is a dict provided by function getMappingDict
	def render(self, mapping):
		for key in mapping.keys():
			rgb = self.convertRGB2Hex(mapping[key])
			mapping[key] = self.formatRenderColor(rgb)

		for key in self.dict_servers:
			value = self.dict_servers[key]
			self.dict_servers[key] = mapping[value]


	# generate an empty/default rectangle data structure
	def genDefaultRect(self):
		return {"verts": None,
				"facecolor_rect": 'white',
				"edgecolor_rect": 'black',
				"label": None,
				"marker": False,
				"edgecolor_marker": 'black'
			   }


	# draw a rectangle
	#
	# {verts: {lb:(left, bottom),rt:(right, top)},
	#  facecolor_rect: 'white',
	#  edgecolor_rect: 'black',
	#  label: [lb:(left, bottom), text:""]
	#  marker: True|False
	#  edgecolor_mark: 'black'
	# }
	def drawRectangle(self, ax, vdict):
		# rect
		vlb = vdict["verts"]["lb"];
		vrt = vdict["verts"]["rt"]
		verts = [vlb, (vlb[0], vrt[1]), vrt, (vrt[0], vlb[1]), (0., 0.)]
		codes = [Path.MOVETO,
		 		 Path.LINETO,
				 Path.LINETO,
		 		 Path.LINETO,
		 		 Path.CLOSEPOLY,
		 		]
		path = Path(verts, codes)
		patch = patches.PathPatch(path, facecolor=vdict["facecolor_rect"], edgecolor=vdict["edgecolor_rect"], lw=1)
		ax.add_patch(patch)
		# label
		if vdict["label"]:
			ax.text(vdict["label"]["lb"][0], vdict["label"]["lb"][1], vdict["label"]["text"])
			# marker
			if vdict["marker"]:
				vfrom = vlb
				vto = [vfrom[0], vfrom[1] + 1]
				aline = Line2D([vfrom[0], vto[0]], [vfrom[1], vto[1]], lw=2, color=vdict["edgecolor_marker"])
				ax.add_line(aline)



	# draw legend
	def legend(self):
		ysize = 1
		xyrate = 10
		xsize = xyrate * ysize
		xlim = xyrate * xsize
		ylim = xyrate * ysize
		fig = plt.figure(figsize=(xsize, ysize))
		ax = fig.add_subplot(111)
		plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.05)
		ax.set_xlim(0, xlim)
		ax.set_ylim(0, ylim)
		plt.axis('off')

		self.drawLegendContent(ax, (xlim, ylim))

		# plt.show()
		fig.savefig(self.filename_rack_legend, transparent=True, dpi=300)

	#
	# update function MUST be called before call the plot function
	# call rackdiag to plot an image of rack
	#
	def plot(self):
		# get mapping dict of colors
		dict_mapping = self.getMappingDict()
		#print "dict mapping, ", dict_mapping
		# render dict_servers with correct color formation
		self.render(dict_mapping)

		# write rendered temporary diag file to disk
		# read original diag file
		rf = open(self.filename_diag, "r");
		template = Template(rf.read())
		scontent = template.render(self.dict_servers)
		rf.close()

		# write rendered diag file to temporary file
		wf = open(self.filename_diag_temp, "w")
		wf.write(scontent)
		wf.close()

		# call rackdiag to plot
		rackdiag("-T{0}".format(self.image_type),
					"-o", self.filename_rack_image, self.filename_diag_temp)

		# draw the image of legend
		self.legend()

		# delete the temporary diag file if needed
		if self.flag_delete_diag_temp:
			rm("-f", self.filename_diag_temp)


	# get random number
	# range is 0.0 ~ 1.0
	# params:
	#   bResetSeed, a Boolean value. True means the seed of Random will be set with current time,
	# 				Flase, do not touch the seed of Random
	def getRandom(self, bResetSeed=False):
		if bResetSeed:
			random.seed(time.time())

		return random.random()


	# guess default location of yaml configuration
	def guessDefaultConfigLocation(self):
		return self.default_home_yaml
	
	# guess default location of diag configuration
	def guessDefaultDiagLocation(self):
		return self.default_home_yaml + "/racks"
	
	# guess default location of image output
	def guessDefaultDiagramLocation(self):
		arr_dir_current = pwd().strip().split("/")
		# current py file: cloudmesh_home/cloudmesh/rack/*.py
		# webui static dir: cloudmesh_home/webui/static
		arr_dir_guess = arr_dir_current[0: -2] + ["webui", "static", "racks"]
		return "/".join(arr_dir_guess)
	
	
	# a helper function
	# get the RGB according to a specific h param
	# ONLY called by sub-class, the valid range of h is [0.0, 2/3]
	def getRGBWithH(self, h):
		(r, g, b) = colorsys.hsv_to_rgb(h, 1, 1)
		arrRGB = [int(round(i * 255)) for i in (r, g, b)]
		return tuple([v if v < 255 else 255 for v in arrRGB])


	# RGB convertion from triple to HEX
	def convertRGB2Hex(self, rgb_tuple):
		(r, g, b) = rgb_tuple
		return "#{0:02X}{1:02X}{2:02X}".format(r, g, b)

	# format render color
	# formation is: [color="#FF00FF"]
	def formatRenderColor(self, str_color):
		return '[color="{0}"]'.format(str_color)



if __name__ == "__main__":
	mytest = BaseClusterMap("india")
	print "=" * 60
	print mytest.dict_servers


