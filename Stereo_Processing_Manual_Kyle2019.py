################################################

#Stereo Processing Manual
#Author: Kyle Strougo
#Email: kstrougo@gmail.com
#Date: 7/1/19
#American Museum of Natural History

###############################################
# Run on linux, assumes NASA Ames Stereo Pipeline and ISIS softwares are downloaded
# Necessary files: Sorted_Final_CTX_2019.csv , asp_v6_singlestereo
# This manual guides you through generating coordinates, a .csv file, a mola.csv file, and runs an image fetch to gather all stereo pairs for desired location and calls NASA ASP Software on those pairs 
###############################################

import numpy as np
import csv
import glob
import os
import time
import datetime

#Takes user raw_input and creates working directory
def start():

	#dp = os.getcwd()
	#asp_path = (dp + "/")
	#folder = raw_input(str("> Type a location name to create a new folder (Olympus_Mons): "))
	#path = (dp + "/" + folder + "/")

	os.system("mkdir " + path)

	W = raw_input(str(" > Do you have your location coordinates? (y/n): "))
	if W == ("y" or "Y"):
		pass
	else:
		#Google earth instructions
		print("--------------------------------")
		print ("")
		print (" 1) Open Google Earth and navigate to Mars")
		print (" 2) Adjust zoom so that latitude and longitude are in 5 degree increments")
		print (" 3) Click on the \"Add Image Overlay\" button at the top and adjust the green box around any 5 degree square then move the box over desired location")
		print (" 4) Navigate to \"Location\" button and record coordinates to nearest degree")
		print (" 5) Subract 360 from East and West coordinates and multiply by -1 (Ex: 115 --> 245)")
		print (" 6) Note coordinates\n")
		print ("------------------------------")

	#Generating CSV
	print ("\n---> Open URL:  http://ode.rsl.wustl.edu/mars/datapointsearch.aspx  ")
	print ("---> Enter coordinates")
	print ("---> Confirm location on the map then click \"Query Count\"")
	print ("---> Under \"CSV Format\" click \"Generate files\" then download the .csv file")
	print ("------------------------------")


	#Moves .csv file from downloads into location folder 
	PEDR = "null"
	while True:
		PEDR = raw_input(str(" > Type \"done\" when .csv file is fully downloaded:  "))
		if PEDR == ("done" or "Done"):
			string_mv = str("mv ~/Downloads/PEDR_*table.csv " + path)
			print ("Running... " + string_mv)
			os.system("mv ~/Downloads/PEDR_*table.csv " + path)
			break
		else:
			pass


	#Generates mola.csv file
	csv_command = ("awk \'BEGIN{FS=\",\"}{elevation = $5 - 3396190; print $2 \",\" $1 \",\" elevation}\' " + path + "PEDR_*.csv >" + Folder + "/" + Folder + "_mola.csv\n") 

	string_csv_command = str(csv_command)
	print ("Running... " + string_csv_command)
	os.system(string_csv_command)



###############################################
#Image Fetch
def image_fetch():

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print("IMAGE FETCH STARTED AT [" + st + "]\n")

	def between(l1,low,high):
		l2 = []
		for i in l1:
			if(i > low and i < high):
				l2.append(l1.index(i))
		return l2

	#Finds the intersecting values of two lists
	def intersect(a, b):
		return list(set(a) & set(b))

	###### IMPORT DATA ######
	fileName = 'Sorted_Final_CTX_2019.csv' #Assumes the file is in the same directory. Otherwise specify directory.
	pathMrox = glob.glob('/hd/na10/isis3/mrox_xxxx_md5.txt/*_md5.txt') #Default path for Krypton
	
	fullPath = os.getcwd() + "/" + fileName

	#Array of image names corresponding to lon and lat
	obs_names = np.loadtxt(fullPath, delimiter = ',', dtype=str, usecols = (0, 1))
	obs_names_L = obs_names[:,0].tolist() #List of left images
	obs_names_R = obs_names[:,1].tolist() #List of right images

	#Import longitudes and latitudes
	print("full path" + fullPath)
	
	LON_LAT = np.genfromtxt(fullPath, delimiter = ',', dtype=float, usecols = (2, 3))
	LON = LON_LAT[:,0].tolist() #List of longitudes
	LAT = LON_LAT[:,1].tolist() #List of latitudes

	###### INPUT LON/LAT ######
	lon1 = raw_input("East Coordinate: ");
	lon2 = raw_input("West Coordinate: ");

	lat1 = raw_input("South Coordinate (as a negative): ");
	lat2 = raw_input("North Coordinate: ");
	
	lon1 = float(lon1)
	lon2 = float(lon2)
	lat1 = float(lat1)
	lat2 = float(lat2)

	###### VALUE SWAP ######
	if lon1 > lon2:
		tempF = lon2
		lon2 = lon1
		lon1 = tempF
	if lat1 > lat2:
		tempF = lat2
		lat2 = lat1
		lat1 = tempF

	###### VALUE SORT ######
	#Sort the longitudes and latitudes using 'between' function
	LON_ind = between(LON,lon1,lon2)
	LAT_ind = between(LAT,lat1,lat2)

	#Find the intersecting values of the longitudes and latitudes using the 'intersect' function
	indexes = intersect(LON_ind, LAT_ind)

	#Sort through the image names for correct stereo pairs
	sort_obs_names_L = [obs_names_L[i] for i in indexes]
	sort_obs_names_R = [obs_names_R[i] for i in indexes]

	IDs = np.column_stack((sort_obs_names_L, sort_obs_names_R))

	#Print sorting completed.
	print('Sorting complete.')

	###### CSV Creation ######
	outfile = open("CTX_" + str(lon1) + "_" + str(lon2) + "_" + str(lat1) + "_" + str(lat2)+ ".csv", "wb")
	writer = csv.writer(outfile)

	[writer.writerow(i) for i in IDs] #Write the file.

	outfile.close()

	#kyle
	currPath = os.getcwd() 
	string_mvCSV = str("mv " + currPath + "/CTX*.csv " + path)
	print ("Running... " + string_mvCSV)
	os.system(string_mvCSV)
	#	

	print('File created.')

	###### LOCATE IMAGES ######
	#Iterate through IMGs and MROx to find images

	URL_list = [] #Create an empty list to append urls to

	for i in np.nditer(IDs, order='C'): #Iterate through the array in C order.
		print ('Locating ' + str(i) + '.IMG...')
		for j in pathMrox:
			with open(j) as currentFile:
				basename = os.path.basename(j) #Define the basename for the files.
				text = currentFile.read()
				if (str(i) in text): #Append the basename and image name to URL if image is found.
					URL_list.append("http://pds-imaging.jpl.nasa.gov/data/mro/mars_reconnaissance_orbiter/ctx/" + basename[:9] + "/data/" + str(i) + '.IMG')
					print('Image located.')

	print (len(URL_list))
	
	len_URL = (len(URL_list))

	###### IMAGE DOWNLOAD ######
	#Can be changed depending on what OS is in use.

	print ("Starting retrieval...")
	homePath = path

	#Linux retrieval
	for i in range(0,len(URL_list),2):
		os.system("mkdir " + path + str(i/2))
		os.chdir(path + str(i/2))
		os.system("wget " + URL_list[i]) 
		os.system("wget " + URL_list[i+1])
		os.chdir(homePath)
		print ("retrieved " + str(i+2) + "/" + str(len(URL_list)))
	#Mac retrieval
	'''
	for i in range(0,len(URL_list),2):
	    os.system("mkdir " + str(i/2))
	    os.chdir(str(i/2))
	    os.system("curl -O " + URL_list[i]) 
	    os.system("curl -O " + URL_list[i+1])
	    os.chdir(homePath)
	    print ("retrieved " + str(i+2) + "/" + str(len(URL_list)))
	''';

###############################################


#ASP Run 
#Moves asp_V6 into each stereo pair folder then runs asp on that pair

	#number of stereo pair folders
	numFolders = ((len_URL//2))
	int_numFolders = (int(numFolders))
	

	print ("--> ASP will be run on each stereo pair folder <--\n")
	print("--> You can follow along with the process in the log file which will be located in your location folder <--\n")

	#iterates through stereo pair folders
	for x in range(int_numFolders):
		
		y = str(x)
		CTX_path = path 
	
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
		print("-> ASP STARTED ON FOLDER " + y + " at ["+ st +"]\n")
		#moves asp into folder
		cp_string = str("cp " + asp_path + "asp_v6_singlestereo " + path + y)
		print ("Running... " + cp_string)
		os.system(cp_string)

		#runs asp on stereo pair, passing necessary paths for asp bash script
		asp_string = str(path + y +"/asp_v6_singlestereo " + CTX_path + " " + (path+y) + " " +y)
		print("Running... " + asp_string)
		os.system(asp_string)
		
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
		print("\n-> ASP FINISHED ON FOLDER " + y + " at [" + st + "]\n")

	print("RELEVANT ASP OUTPUT for each folder: \n")

	print("1)  log : Each completed stereo pair will have a log file containing all the output for the process. This file is incredibly useful for troubleshooting, as it can tell you what went wrong and when")
	print("2)  productb/product-PC.tif : The result of running the command \"stereo\". This is a Point Cloud File, and is used to then generate the heightmap and/or orthoimage if desired")
	print("3)  dem_align: The folder containing the products of pc_align, most notably the align-trans_reference.tif file which is then used to generate the DEM")
	print("4)  DEM_high-DEM-adj.tif : The final product of the asp_v5_singlestereo script. This is a height corrected heightmap GeoTiff for the particular stereopair. It can then be mosaiced with other heightmaps or be left on its own")
	print("5)  DEM_final-DRG.tif in some folders. This is necessary for further image generation\n")
	
	print("TROUBLESHOOTING: If you are not getting some of these files you may need to increase displacement in the ASP script")
	print("- To increase displacement open up the asp_v6_singlestereo script and increase the \"maxd\" value at the top (avoid going above 5000)")
	print("Save and re-run this program or manually run the asp on that folder (/HD/na10/isis3/Kyle/Olympus_Mons/3/asp_v6_singlestereo)")
	print("-------------------------------")

####################

def asp_run():
	

	print ("\n--> ASP will be run on each stereo pair folder <--\n")
	print("--> You can follow along with the process in the log file which will be located in your location folder <--\n")

	#iterates through stereo pair folders
	for x in range(first, int_numFolders, 1):
		
		y = str(x)
		CTX_path = path 
	
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
		print("-> ASP STARTED ON FOLDER " + y + " at ["+ st +"]\n")
		#moves asp into folder
		cp_string = str("cp " + asp_path + "asp_v6_singlestereo " + path + y)
		print ("Running... " + cp_string)
		os.system(cp_string)

		#runs asp on stereo pair, passing necessary paths for asp bash script
		asp_string = str(path + y +"/asp_v6_singlestereo " + CTX_path + " " + (path+y) + " " +y)
		print("Running... " + asp_string)
		os.system(asp_string)
		
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
		print("\n-> ASP FINISHED ON FOLDER " + y + " at [" + st + "]\n")

	print("RELEVANT ASP OUTPUT for each folder: \n")

	print("1)  log : Each completed stereo pair will have a log file containing all the output for the process. This file is incredibly useful for troubleshooting, as it can tell you what went wrong and when")
	print("2)  productb/product-PC.tif : The result of running the command \"stereo\". This is a Point Cloud File, and is used to then generate the heightmap and/or orthoimage if desired")
	print("3)  dem_align: The folder containing the products of pc_align, most notably the align-trans_reference.tif file which is then used to generate the DEM")
	print("4)  DEM_high-DEM-adj.tif : The final product of the asp_v5_singlestereo script. This is a height corrected heightmap GeoTiff for the particular stereopair. It can then be mosaiced with other heightmaps or be left on its own")
	print("5)  DEM_final-DRG.tif in some folders. This is necessary for further image generation\n")
	
	print("TROUBLESHOOTING: If you are not getting some of these files you may need to increase displacement in the ASP script")
	print("- To increase displacement open up the asp_v6_singlestereo script and increase the \"maxd\" value at the top (avoid going above 5000)")
	print("Save and re-run this program or manually run the asp on that folder (/HD/na10/isis3/Kyle/Olympus_Mons/3/asp_v6_singlestereo)")
	print("-------------------------------")


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



	#Final file generation - heightmap vrt's
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
	#GOOD TILL HERE


	#Final File Generation - image vrt's 
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

####
numFolders = ""
Folder = ""
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print ("\nPROGRAM STARTED AT [" + st + "]\n")
			
print ("	STEREO PROCESSING MANUAL 2019\n")
print ("--> Move this file into the the desired directory for your new location folder and run the program <--\n")
print ("--> Also move the  \"Sorted_Final_CTX_2019.csv\" and \"asp_v6_singlestereo\" into the same working directory <--\n\n")

dp = os.getcwd()
asp_path = (dp + "/")

Z = raw_input(str(" > Do you need to create a folder for your location? (y/n): "))	

if Z == ("n" or "N"):
	R = raw_input(str(" > Do you want to go to a different directory? (y/n): "))
	if R == ("y" or "Y"):
		path = raw_input(str(" > Type full directory path (../Olympus_Mons/): "))
	else:
		Folder = raw_input(str(" > Type an existing folder name in the current directory (Olympus_Mons): "))
		path = (dp + "/" + Folder + "/")
else:
	Folder = raw_input(str(" > Type a location name to create a new folder (Olympus_Mons): "))
	path = (dp + "/" + Folder + "/")

	start()
	image_fetch()
	mosaic()
	height_mosaic()
	image_mosaic()
	info()

#path = (dp + "/" + Folder + "/")

print ("-------------------------------")

###

if __name__ == '__main__':
	functions = []

	print("Options:\n")
	print("1) Image Fetch / Run ASP")
	print("2) Run ASP on select folders")
	print("3) Height map mosaic")
	print("4) Image map mosaic")
	print("5) Generation of .info file\n")

	while True:

		x = int(input(" > Type what you want to do *one at a time* (type \"-1\" when finished): "))
		if x == (-1):
			break
		else:
			functions.append(x)

	for i in functions:
		if i == (1):
				image_fetch()
		if i == (2):
				first = int(input(" > Type the folder to start on (type 0 if no preference) "))
				int_numFolders = int(input(" > Type the number of stereo pair folders: "))
				asp_run()
		if i == (3):
				if (numFolders and Folder) == (""): 
					numFolders = input(str(" > Type the number of stereo pair folders: "))
					Folder = raw_input(" > Type the folder name: ")
				mosaic()
				height_mosaic()
		if i == (4):
				if  (numFolders and Folder) == (""):
					numFolders = input(str(" > Type the number of stereo pair folders: "))
					Folder = raw_input(" > Type the folder name: ")
				mosaic()
				image_mosaic()
		if i == (5):
				info()

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	print("\n-> Relevant Files for Openspace: \n\n")
	print(" 1) " + Folder + "_heightmap.vrt")
	print(" 2) " + Folder + "_texture.vrt")
	print(" 3) " + Folder + "_heightmap_longlat.tif")
	print(" 4) " + Folder + "_texture_longlat.tif")
	print(" 5) " + Folder + ".info\n")
			
	print ("\nPROGRAM FINISHED at [" + st + "]\n")

	



