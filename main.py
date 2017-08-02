"""Tada converts emotes from Pidgin to several other formats"""

import mimetypes
import re
from argparse import ArgumentParser
from os import path

from PIL import Image
from yapsy.PluginManager import PluginManager

# Create the emote pack container
class EmotePack(object):
    """Defines the metadata and content of an emote pack"""
    name = "Untitled Pack"
    desc = ""
    author = ""
    version = ""
    icon = ""
    emotelist = []
    path = ""
    output = ""
    filename = ""

class Emote(object):
    """A single emote object in an emote pack"""
    filename = ""
    filetype = ""
    shortcuts = []
    width = 0
    height = 0

optp = ArgumentParser()

optp.add_argument("-i", "--input", dest="inputdir", help="Input folder containing the emote pack")
optp.add_argument("-o", "--output", dest="outputdir", help="Output folder for converted packs")
optp.add_argument("-n", "--name", dest="name", help="Filename prefix")
optp.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Verbose output")

opts, args = optp.parse_args()

inputDir = "input"
outputDir = "output"
verbose = False

if opts.inputdir:
    inputDir = opts.inputdir

if opts.outputdir:
    outputDir = opts.outputdir

if opts.verbose:
    verbose = True

if not path.isdir(inputDir):
    print("Input directory doesn't exist")
    exit(1)

if not path.isdir(outputDir):
    print("Output directory doesn't exist")
    exit(1)

inputData = open(path.join(inputDir, "theme"), 'r')
inputData = inputData.read()

# Instantiate and fill the pack metadata
InputPack = EmotePack()

InputPack.path = inputDir
InputPack.output = outputDir

try:
    InputPack.name = re.findall(r"Name=(.*)", inputData)[-1]
except IndexError:
    print("Couldn't find a name, skipping")
    pass

try:
    InputPack.desc = re.findall(r"Description=(.*)", inputData)[-1]
except IndexError:
    print("Couldn't find a description, skipping")
    pass

try:
    InputPack.author = re.findall(r"Author=(.*)", inputData)[-1]
except IndexError:
    print("Couldn't find an author, skipping")
    pass

if opts.name:
    InputPack.filename = opts.name
else:
    InputPack.filename = InputPack.name

# Reopen the pack in line mode and skip the header lines
inputFile = open(path.join(inputDir, "theme"), 'r')
inputFile = inputFile.readlines()[6:]

# Fill the container with Emotes
for line in inputFile:
    if verbose:
        print(line)

    if line.startswith('!'):
        line = line.replace('!', '')    # Strip off the leading !
    line = line.strip().split()             # Split into tokens

    thisEmote = Emote()
    thisEmote.filename = line[0]    # Identify the file and its type, as required for some formats.
    thisEmote.filetype = mimetypes.guess_type(line[0])[0]
    thisEmote.shortcuts = line[1:]

    try:                # Dimensions are required for phpBB
        im = Image.open(path.join(inputDir, thisEmote.filename))
        thisEmote.width, thisEmote.height = im.size
    except IOError:     # If the file doesn't exist, lets not package it, either
        continue

    InputPack.emotelist.append(thisEmote)

pm = PluginManager(
    directories_list=["templates", path.join(path.dirname(path.abspath(__file__)), "templates")],
    plugin_info_ext="plug"
)
pm.collectPlugins()

for backend in pm.getAllPlugins():
    backend.plugin_object.build(InputPack)
