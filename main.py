import re
import mimetypes
from yapsy.PluginManager import PluginManager
from os import path
from PIL import Image
from optparse import OptionParser


# Create the emote pack container
class EmotePack(object):
    name = "Untitled Pack"
    desc = ""
    author = ""
    version = ""
    icon = ""
    emotelist = []
    path = ""


class Emote(object):
    filename = ""
    filetype = ""
    shortcuts = []
    width = 0
    height = 0

optp = OptionParser()

optp.add_option("-i", "--input", dest="inputdir", help="Input folder containing the emote pack")

opts, args = optp.parse_args()

inputDir = "input"

if opts.inputdir:
    inputDir = opts.inputdir

if not path.isdir(inputDir):
    print("Input directory doesn't exist")
    exit(1)

inputData = open(path.join(inputDir, "theme"), 'r')
inputData = inputData.read()

# Instantiate and fill the pack metadata
InputPack = EmotePack()

InputPack.path = inputDir

try:
    InputPack.name = re.findall(r"Name=(.*)", inputData)[-1]
except IndexError:
    print "Couldn't find a name, skipping"
    pass

try:
    InputPack.desc = re.findall(r"Description=(.*)", inputData)[-1]
except IndexError:
    print "Couldn't find a description, skipping"
    pass

try:
    InputPack.author = re.findall(r"Author=(.*)", inputData)[-1]
except IndexError:
    print "Couldn't find an author, skipping"
    pass

# Reopen the pack in line mode
inputFile = open(path.join(inputDir, "theme"), 'r')
inputFile = inputFile.readlines()

# Fill the container with Emotes
for line in inputFile:
    if line.startswith('!'):
        line = line.replace('!', '')    # Strip off the leading !
        line = line.split()             # Split into tokens

        thisEmote = Emote()
        thisEmote.filename = line[0]    # Identify the file and its type, as required for some formats.
        thisEmote.filetype = mimetypes.guess_type(line[0])[0]
        thisEmote.shortcuts = line[1:]

        try:                # Dimensions are required for phpBB
            im = Image.open(path.join("input", thisEmote.filename))
            thisEmote.width, thisEmote.height = im.size
        except IOError:     # If the file doesn't exist, lets not package it, either
            continue

        InputPack.emotelist.append(thisEmote)

pm = PluginManager(
    directories_list=["templates"],
    plugin_info_ext="plug"
)
pm.collectPlugins()

for backend in pm.getAllPlugins():
    backend.plugin_object.build(InputPack)
