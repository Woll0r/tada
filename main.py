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

def main():
    """Main program execution"""
    if not path.isdir(inputdir):
        print("Input directory doesn't exist")
        exit(1)

    if not path.isdir(outputdir):
        print("Output directory doesn't exist")
        exit(1)

    inputdata = open(path.join(inputdir, "theme"), 'r')
    inputdata = inputdata.read()

    # Instantiate and fill the pack metadata
    inputpack = EmotePack()

    inputpack.path = inputdir
    inputpack.output = outputdir

    try:
        inputpack.name = re.findall(r"Name=(.*)", inputdata)[-1]
    except IndexError:
        print("Couldn't find a name, skipping")
        pass

    try:
        inputpack.desc = re.findall(r"Description=(.*)", inputdata)[-1]
    except IndexError:
        print("Couldn't find a description, skipping")
        pass

    try:
        inputpack.author = re.findall(r"Author=(.*)", inputdata)[-1]
    except IndexError:
        print("Couldn't find an author, skipping")
        pass

    if opts.name:
        inputpack.filename = opts.name
    else:
        inputpack.filename = inputpack.name

    # Reopen the pack in line mode and skip the header lines
    inputfile = open(path.join(inputdir, "theme"), 'r')
    inputfile = inputfile.readlines()[6:]

    # Fill the container with Emotes
    for line in inputfile:
        if verbose:
            print(line)

        if line.startswith('!'):
            line = line.replace('!', '')    # Strip off the leading !
        line = line.strip().split()             # Split into tokens

        thisemote = Emote()
        # Identify the file and its type, as required for some formats.
        thisemote.filename = line[0]
        thisemote.filetype = mimetypes.guess_type(line[0])[0]
        thisemote.shortcuts = line[1:]

        # Dimensions are required for phpBB
        try:
            im = Image.open(path.join(inputdir, thisemote.filename))
            thisemote.width, thisemote.height = im.size
        except IOError:
            # If the file doesn't exist, lets not package it, either
            continue

        inputpack.emotelist.append(thisemote)

    pm = PluginManager(
        directories_list=["templates",
                          path.join(path.dirname(path.abspath(__file__)),
                                    "templates")
                         ],
        plugin_info_ext="plug"
    )
    pm.collectPlugins()

    for backend in pm.getAllPlugins():
        backend.plugin_object.build(inputpack)

if __name__ == '__main__':
    argp = ArgumentParser()

    argp.add_argument("-i", "--input",
                      dest="inputdir",
                      help="Input folder containing the emote pack")
    argp.add_argument("-o", "--output",
                      dest="outputdir",
                      help="Output folder for converted packs")
    argp.add_argument("-n", "--name",
                      dest="name",
                      help="Filename prefix")
    argp.add_argument("-v", "--verbose",
                      dest="verbose",
                      action="store_true",
                      help="Verbose output")

    opts = argp.parse_args()

    inputdir = "input"
    outputdir = "output"
    verbose = False

    if opts.inputdir:
        inputdir = opts.inputdir

    if opts.outputdir:
        outputdir = opts.outputdir

    if opts.verbose:
        verbose = True

    main()
