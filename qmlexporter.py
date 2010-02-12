#!/usr/bin/env python
# Author: Jens Bache/Wiig
# Copyright 2010 Jens Bache-Wiig
# License: GPL v3
# Version 0.1
# GIMP plugin to export layers as QML

from gimpfu import *
import os

gettext.install("gimp20-python", gimp.locale_directory, unicode = True)

def export_qml(image, qmlname, path):
        qmlfilename = os.path.join(path, qmlname + '.qml')
	imagedirectory = qmlname + "_images"

	# Create a subfolder for the image content
        imagepath = os.path.join(path, imagedirectory);
	if not os.path.isdir(imagepath):
	    os.mkdir(imagepath)

	f = open(qmlfilename, 'w')
        f.write('import Qt 4.6\n')
        f.write('Rectangle {\n')
	copy = image.duplicate()

	i = len(copy.layers) - 1	
	while i >= 0 :
		layer = copy.layers[i]
		layer.visible = 1
		layername = layer.name.lower()
		layername = layername.replace(' ', '_')
		layername = layername.replace('#', '__')

		name = imagepath + "/" + layername + ".png"
		fullpath = os.path.join(path, name);
		opacity = layer.opacity / 100.0

		# Write out the element
		f.write('    Image {\n')
		f.write('        id:' + layername +'\n')

		if opacity < 1.0: # Only dump opacity if it is required
	        	f.write('        opacity: %s' % opacity +'\n')

		f.write('        source:\"' + imagedirectory + "/" + layername + '.png\"\n')
		f.write('        x:%s ; y:%s' % layer.offsets + '\n')
		f.write('        width:%s '   % layer.width + '\n')
		f.write('        height:%s '  % layer.height + '\n')

		# Store the layer as a .png
		pdb.file_png_save(copy, layer, fullpath, name, 0, 9, 1, 1, 1, 1, 1)
		f.write('    }\n')
		i = i - 1
        f.write('}\n')
        f.close()
 
register(
    proc_name = ("python-fu-export-qml"),
    blurb = ("Export layers to a QML document"),
    help = ("Export layers as a QML document."),
    author = ("Jens Bache-Wiig"),
    copyright = ("Jens Bache-Wiig"),
    date = ("2010"),
    label = ("Export to _QML"),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "image", "Image", None),
        (PF_STRING, "qmlname", "QML Element", "MyElement"),
        (PF_DIRNAME, "path", "Save QML to this directory", os.getcwd()),],
    results=[],
    function=(export_qml),
    menu=("<Image>/File"),
    domain=("gimp20-python", 
    gimp.locale_directory)
)

main()
