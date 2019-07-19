import time
import os
import datetime


path = "/"
asp_path = "/"

#ASP Run 
#Moves asp_V6 into each stereo pair folder then runs asp on that pair


#number of stereo pair folders
numFolders = ((24//2))
int_numFolders = (int(numFolders))
#path to asp

print ("--> ASP will be run on each stereo pair folder <--\n")
print("--> You can follow along with the process in the log file which will be located in your location folder <--\n")
#iterates through stereo pair folders
for x in range(12, 6, -1):
	
	y = str(x)
	CTX_path = path 

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	print("-> ASP STARTED ON FOLDER " + y + " at ["+ st +"]\n")
	#moves asp into folder
	cp_string = str("cp " + asp_path + "asp_v6_singlestereo " + path + y)
	print ("Copy ASP: " + cp_string)
	os.system(cp_string)

	#runs asp on stereo pair, passing necessary paths for asp bash script
	asp_string = str(path + y +"/asp_v6_singlestereo " + CTX_path + " " + (path+y) + " " +y)
	print("Execute ASP: " + asp_string)
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