import time
import os
import datetime


path = "/"
asp_path = "/"
numFolders = (0)

#Heightmap Mosaicing

print("--> Heightmap Mosaicing <--")
print("-- This next step utilizes the \"Stereo_Gui\" to view the height files (DEM_high-DEM-adj.tif) and image files (DEM_final-DRG.tif) from each folder")
print ("-- Stereo_Gui will open all layers once you go to \"View\" and click \"Overlay Georeferenced Images\" and you will evaluate each layer and **note which ones to keep**")
print("-- You can also enable the \"Hillshade\" (only for heightmap) button in the same dropdown")
print("")

ready = "null"
while True:
	ready = raw_input(str(" > Type \"ready\" to begin mosaicing process:  "))
	if ready == ("ready" or "Ready"):
		break
	else:
		pass

#Generates command to open stereo_gui for all heightmap folders 
str_numFolders = str(numFolders)
str_mosaic = str("stereo_gui " + path + "{0.." + str_numFolders + "}/DEM_high-DEM-adj.tif")
print ("Running... " + str_mosaic)
os.system(str_mosaic)
print ("done -----------------------")

print ("--> Next you will enter the valid layer numbers that you wish to keep for your height map mosaic")
ready = "null"
while True:
	ready = raw_input(str(" > Type \"ready\" to begin mosaicing process:  "))
	if ready == ("ready" or "Ready"):
		break
	else:
		pass

#Takes user input for valid height layers 
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

full_command_layer = ("dem_mosaic "+ dem_mosaic + " -o " + Folder + "_heightmap")
path_command_layer = (full_command_layer)
str_dem_height = str(path_command_layer)

print("\nRunning.. " + str_dem_height)
os.system(str_dem_height)

print ("--> Next you will enter the valid layer numbers that you wish to keep for your image map mosaic")
ready = "null"
while True:
	ready = raw_input(str(" > Type \"ready\" to begin mosaicing process:  "))
	if ready == ("ready" or "Ready"):
		break
	else:
		pass

#Takes user input for valid height layers 
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

full_command_layer_image = ("dem_mosaic " + dem_mosaic_image + " -o " + Folder + "_texture")
path_command_layer_image = (path + full_command_layer_image)
str_dem_image = str(path_command_layer_image)

print("\nRunning.. " + str_dem_image)
os.system(str_dem_image)
#GOOD TILL HERE

#Hole filling command
print("\nExecuting hole filling")
#gdal_fillnodata.py -md 25 -si 1 Ganges_heightmap-tile-0.tif
hole_fill = ("gdal_fillnodata.py -md 25 -si 1 " + path + Folder + "_heightmap-tile-0.tif")
str_hole_fill = str(hole_fill)
print("\nRunning... " + str_hole_fill)
os.system(str_hole_fill)


#Final file generation - heightmap vrt's
print("FINAL FILE GENERATION \n")

height_vrt1 = ("gdalwarp -t_srs \"+proj=longlat\" " + path + Folder + "_heightmap-tile-0.tif "+ Folder + "_heightmap_longlat.tif")
str_height_vrt1 = str(height_vrt1)
print("\nRunning... " + str_height_vrt1)
os.system(str_height_vrt1)

height_vrt2 = ("gdalbuildvrt " + path + Folder + "_heightmap.vrt -te -180 -90 180 90 " + Folder + "_heightmap_longlat.tif")
str_height_vrt2 = str(height_vrt2)
print("\nRunning... " + str_height_vrt2)
os.system(str_height_vrt2)

#Final File Generation - image vrt's 
image_vrt1 = ("gdalwarp -t_srs \"+proj=longlat\" " + path + Folder + "_texture-tile-0.tif " + Folder + "_texture_longlat.tif")
str_image_vrt1 = str(image_vrt1)
print("\nRunning... " + str_image_vrt1)
os.system(str_image_vrt1)

image_vrt2 = ("gdalbuildvrt " + path + Folder + "_texture.vrt -te -180 -90 180 90 -addalpha " + Folder + "_texture_longlat.tif")
str_image_vrt2 = str(image_vrt2)
print("\nRunning... " + str_height_vrt2)
os.system(str_image_vrt2)

#Generation of .info file for Openspace
print("\nGenerating the .info file for Openspace\n")
info = ("touch " + path + Folder + ".info")
str_info = str(info)
print("Running... " + str_info)
os.system(str_info)

print("\nIn your location folder, open up the .info file and match the below format")
print("Save and exit\n")
print("** The \"ColorFile\" should be the same as your image.vrt file name and the \"HeightFile\" should match your heightmap.vrt file name **")

print("Name=\"Olympus Mons\"")
print("Identifier=\"olympus_mons\"")
print("ColorFile=\"Olympus_Mons_mapro_texture.vrt\"")
print("HeightFile=\"Olympus_Mons_heightmap.vrt\"")

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

print ("\nPROGRAM FINISHED at [" + st + "]")



