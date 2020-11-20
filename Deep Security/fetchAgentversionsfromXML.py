from __future__ import print_function
from time import sleep
import os
import sys, warnings

def auto_install():
        print("Just installing required modules")
        print("if they do not already exist")
        os.system(" pip install requests ")
        print("\nRequirements installed.\n")

try:
	import xml.etree.ElementTree as ET
	import requests
	import time

except:
    auto_install()

def loadXML(): 
  
    # url of xml
    url = 'http://files.trendmicro.com/products/deepsecurity/en/DeepSecurityInventory_en.xml'
  
    # creating HTTP response object from given url 
    print("Loading XML...")
    resp = requests.get(url) 
  
    # saving the xml file 
    with open('ds_versions.xml', 'wb') as f: 
        f.write(resp.content) 

def sortXML():
	tree = ET.parse('ds_versions.xml')
	root = tree.getroot()

	# all items data
	full_list = []
	ds_version_list = []
	print("Sorting XML...")
	for elem in root:
	    for subelem in elem:
	        full_list.append(str(subelem.text))

	for i in full_list:
			if 'Deep Security Agent' in i:
				ds_version_list.append(i)

	prefinal_sort = set(ds_version_list)
	final_sort = prefinal_sort

	return final_sort

def saveToLogFile(list_version):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	print("Exporting to a log file...")
	sleep(3)

	log = 'logs'
	filename = log + "/" + timestr + '-versions.log'


	try:
	    os.mkdir(log)
	except OSError:
	    print ("Folder already exists!")
	else:
	    print ("Successfully created the directory %s " % log)

	with open(filename, 'w') as f:
		print("Total number of entries: " + str(len(list_version)), file=f)
		for i in list_version:
				print(i, file=f)  # Python 3.x

	print("Saving log file...")
	os.remove("ds_versions.xml")
	print("Filename: " + filename)
	print("Done.")


print("Welcome to Deep Security Version listing")
loadXML()
pull = sortXML()
saveToLogFile(pull)