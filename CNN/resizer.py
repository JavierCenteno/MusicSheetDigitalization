#!/usr/bin/python
from PIL import Image
import os, sys

def resize():
	path = "data/train/"
	dirs = os.listdir(path)
	for folder in dirs:
		newPath = path + folder
		dirs = os.listdir(newPath)
		for item in dirs:
			file = newPath+"/"+item
			if os.path.isfile(file):
				im = Image.open(file)
				f, e = os.path.splitext(file)
				imResize = im.resize((50,150), Image.ANTIALIAS)
				imResize.save(f + '.png', 'PNG', quality=90)
resize()