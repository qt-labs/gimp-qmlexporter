#!/usr/bin/env python
# Author: Jens Bache/Wiig
# Copyright 2010 Jens Bache-Wiig
# License: GPL v3
# Version 0.1
# GIMP plugin to export layers as QML

from gimpfu import *
import os

gettext.install("gimp20-python", gimp.locale_directory, unicode = True)

imagedirectory = ""
imagepath = ""
path = ""

def format_color(color) :
	return "Qt.rgba(%i, %i, %i, %i)" % (color[0]/255.0, 
					     color[1]/255.0, 
					     color[2]/255.0,
					     color[3]/255.0)

def dump_common_properties(layer, layername, f) :
	f.write('        id:' + layername +'\n')
	opacity = layer.opacity / 100.0
	if opacity < 1.0: # Only dump opacity if it is required
        	f.write('        opacity: %s' % opacity +'\n')
	f.write('        x:%s ; y:%s' % layer.offsets + '\n')
	f.write('        width:%s '   % layer.width + '\n')
	f.write('        height:%s '  % layer.height + '\n')

def dump_text_element(layer, layername, f):
	f.write('    Text {\n')
	f.write('        text:\'%s\' '   %  pdb.gimp_text_layer_get_text(layer) + '\n')
	f.write('        font.pixelSize:%i '   %  pdb.gimp_text_layer_get_font_size(layer)[0] + '\n')
	color = pdb.gimp_text_layer_get_color(layer)
	f.write('        color:' + format_color(color) + '\n')
	dump_common_properties(layer, layername, f)
	f.write('    }\n')

def dump_image_element(layer, layername, f, image):
	global imagedirectory
	global imagepath
	global path
	opacity = layer.opacity / 100.0
	name = imagepath + "/" + layername + ".png"
	fullpath = os.path.join(path, name);
	
	# Write out the element
	f.write('    Image {\n')
	f.write('        source:\"' + imagedirectory + "/" + layername + '.png\"\n')

	# Dump common properties
	dump_common_properties(layer, layername, f)

	# Store the layer as a .png
	pdb.file_png_save(image, layer, fullpath, name, 0, 9, 1, 1, 1, 1, 1)
	f.write('    }\n')

# Removes non-usable id-characters from layer names
def fix_name(name) :
	fixedname = name.lower()
	fixedname = fixedname.replace(' ', '_')
	fixedname = fixedname.replace('#', '__')
	fixedname = fixedname.replace('!', '___')
	return fixedname

def export_qml(image, qmlname, path, flatten):
	global imagepath
	global imagedirectory
        qmlfilename = os.path.join(path, qmlname + '.qml')
	imagedirectory = qmlname + "_images"

	# Create a subfolder for the image content
        imagepath = os.path.join(path, imagedirectory);
	if not os.path.isdir(imagepath):
	    os.mkdir(imagepath)

	f = open(qmlfilename, 'w')
        f.write('import Qt 4.7\n')
        f.write('Rectangle {\n')
	copy = image.duplicate()
	
	layercount = len(copy.layers)
	# We give the base element the same size as the background
	bglayer = copy.layers[layercount-1]
	f.write('    width:%s '   % bglayer.width + '\n')
	f.write('    height:%s '  % bglayer.height + '\n')
			
	i = layercount - 1	
	while i >= 0 :
		layer = copy.layers[i]
		layer.visible = 1
		layername = fix_name(layer.name)

		if pdb.gimp_drawable_is_text_layer(layer) and not flatten :
			dump_text_element(layer, layername, f)
		else :
			dump_image_element(layer, layername, f, copy)

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
        (PF_STRING, "qmlname", "QML Element Name:", "MyElement"),
        (PF_DIRNAME, "path", "Save QML to this Directory", os.getcwd()),
	(PF_BOOL, "flatten", "Convert text to image:", 0),
	],
    results=[],
    function=(export_qml),
    menu=("<Image>/File"),
    domain=("gimp20-python", 
    gimp.locale_directory)
)

main()
