################################################

# Image and Height Map Mosaicing 
# Author: Kyle Strougo
# Email: kstrougo@gmail.com
# Date: 7/1/19
# American Museum of Natural History / Openspace NASA Grant

###############################################
# Run on linux, assumes NASA Ames Stereo Pipeline and ISIS softwares are downloaded
# Necessary files: image/height dems
# This program guides you through image/height map mosaicing and generation of necessary files for Openspace
###############################################

import time
import os
import datetime

########################################
#MOSAICING
def mosaic():
	print("\n--> Mosaicing Process <--")
	print("-- This next step utilizes the \"Stereo_Gui\" to view the height files (DEM_high-DEM-adj.tif) and image files (DEM_final-DRG.tif) from each folder")
	print ("-- Stereo_Gui will open all layers once you go to \"View\" and click \"Overlay Georeferenced Images\" and you will evaluate each layer and **note which ones to keep**")
	print("-- You can also enable the \"Hillshade\" button (only for heightmap) in the same dropdown")
	print("")


#HEIGHT MOSAIC
def height_mosaic():
	ready = "null"
	while True:
		ready = raw_input(str(" > Type \"ready\" to preview all height layers (note which to keep):  "))
		if ready == ("ready" or "Ready"):
			break
		else:
			pass


	#Generates command to open stereo_gui for all heightmap folders 
	str_numFolders = str(numFolders)
	str_mosaic = str("stereo_gui " + path + "{0.." + str_numFolders + "}/DEM_high-DEM-adj.tif")
	print ("Running... " + str_mosaic)
	os.system(str_mosaic)
	print ("-----------------------")



	print ("--> Next you will enter the valid layer numbers that you wish to keep for your height map mosaic")
	ready = "null"
	while True:
		ready = raw_input(str(" > Type \"ready\" to begin mosaicing process:  "))
		if ready == ("ready" or "Ready"):
			break
		else:
			pass


	#Takes user input for valid HEIGHT layers 
	array_layers = []
	while True:
	  map_layers = input((" > Type the layers you want to keep **one at a time** (type \"-1\" when finished): "))
	  if map_layers == (-1):
	    break
	  else:
	    array_layers.append(map_layers)


	#For loop generates heightmap dem_mosaic command with kept layers 
	dem_mosaic = ""
	for layer in array_layers:
		str_layer = str(layer)	
		command_layer = (path + str_layer + "/DEM_high-DEM-adj.tif ")
		dem_mosaic = (dem_mosaic + command_layer)

	full_command_layer = ("dem_mosaic "+ dem_mosaic + " -o " + path + Folder + "_heightmap")
	path_command_layer = (full_command_layer)
	str_dem_height = str(path_command_layer)
	
	print("\nRunning.. " + str_dem_height)
	os.system(str_dem_height)


	#Height map hole filling 
	print("\nExecuting hole filling")
	#gdal_fillnodata.py -md 25 -si 1 Ganges_heightmap-tile-0.tif
	hole_fill = ("gdal_fillnodata.py -md 25 -si 1 " + path + Folder + "_heightmap-tile-0.tif")
	str_hole_fill = str(hole_fill)
	print("\nRunning... " + str_hole_fill)
	os.system(str_hole_fill)



	#Final file generation - height map vrt
	print("\nFINAL HEIGHT FILE GENERATION\n")
	
	height_vrt1 = ("gdalwarp -t_srs \"+proj=longlat\" " + path + Folder + "_heightmap-tile-0.tif " + path + Folder + "_heightmap_longlat.tif")
	str_height_vrt1 = str(height_vrt1)
	print("\nRunning... " + str_height_vrt1)
	os.system(str_height_vrt1)

	height_vrt2 = ("gdalbuildvrt " + path + Folder + "_heightmap.vrt -te -180 -90 180 90 " + path + Folder + "_heightmap_longlat.tif")
	str_height_vrt2 = str(height_vrt2)
	print("\nRunning... " + str_height_vrt2)
	os.system(str_height_vrt2)


	print ("-----------------------")

#######################################

#IMAGE MOSAIC

def image_mosaic():
	ready = "null"
	while True:
		ready = raw_input(str(" > Type \"ready\" to preview all image layers (note which to keep):  "))
		if ready == ("ready" or "Ready"):
			break
		else:
			pass

	#Generates command to open stereo_gui for all image folders 
	str_numFolders = str(numFolders)
	str_mosaic = str("stereo_gui " + path + "{0.." + str_numFolders + "}/DEM_final-DRG.tif")
	print ("Running... " + str_mosaic)
	os.system(str_mosaic)
	print ("-----------------------")



	print ("--> Next you will enter the valid layer numbers that you wish to keep for your image map mosaic")
	ready = "null"
	while True:
		ready = raw_input(str(" > Type \"ready\" to begin mosaicing process:  "))
		if ready == ("ready" or "Ready"):
			break
		else:
			pass


	#Takes user input for valid IMAGE layers 
	array_layers = []
	while True:
	  map_layers = input((" > Type the layers you want to keep **one at a time** (type \"-1\" when finished): "))
	  if map_layers == (-1):
	    break
	  else:
	    array_layers.append(map_layers)


	#For loop generates image dem_mosaic command with kept layers
	dem_mosaic_image = ""
	for layer in array_layers:
	  str_layer = str(layer)
	  command_layer_image = (path + str_layer + "/DEM_final-DRG.tif ")
	  dem_mosaic_image = (dem_mosaic_image + command_layer_image)

	full_command_layer_image = ("dem_mosaic " + dem_mosaic_image + " -o " + path + Folder + "_texture")
	path_command_layer_image = (full_command_layer_image)
	str_dem_image = str(path_command_layer_image)

	print("\nRunning.. " + str_dem_image)
	os.system(str_dem_image)
	


	#Final File Generation - image vrt
	print("\nFINAL IMAGE FILE GENERATION")	

	image_vrt1 = ("gdalwarp -t_srs \"+proj=longlat\" " + path + Folder + "_texture-tile-0.tif " + path + Folder + "_texture_longlat.tif")
	str_image_vrt1 = str(image_vrt1)
	print("\nRunning... " + str_image_vrt1)
	os.system(str_image_vrt1)
	
	image_vrt2 = ("gdalbuildvrt " + path + Folder + "_texture.vrt -te -180 -90 180 90 -addalpha " + path + Folder + "_texture_longlat.tif")
	str_image_vrt2 = str(image_vrt2)
	print("\nRunning... " + str_image_vrt2)
	os.system(str_image_vrt2)


#Generation of .info file for Openspace
def info():
	print("\nGenerating the .info file for Openspace\n")
	info = ("touch " + path + Folder + ".info")
	str_info = str(info)
	print("Running... " + str_info)
	os.system(str_info)
	
	I = open(path + Folder + ".info", "w")
	str_folder = str(Folder)
	I.write("Name=\"" + str_folder + " CTX\"")
	I.write("\nIdentifier=\"" + str_folder + "\"") 
	I.write("\nColorFile=\"" + str_folder + "_texture.vrt\"")
	I.write("\nHeightFile=\"" + str_folder + "_heightmap.vrt\"")
	I.close()
	
	print(str_folder + ".info file generated")

dp = os.getcwd()
asp_path = (dp +"/")
Folder = raw_input(str(" > Type an existing folder name in the current directory (Olympus_Mons): "))
path = (asp_path + Folder + "/")

mosaic()
height_mosaic()
image_mosaic()
info()


