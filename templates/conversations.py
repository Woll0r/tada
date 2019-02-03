"""Conversations plugin for Tada"""

import json
import zipfile
from os.path import isfile
from PIL import Image
from io import BytesIO

from yapsy.IPlugin import IPlugin

class ConversationsBackend(IPlugin):
    """Conversations plugin for Tada"""
    pack = None

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Conversations] Building zip...")
        self.makezip()

    def makezip(self):
        """Create the emote zip file"""
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-conversations.zip", 'w')
        emotes = {}
        for emote in self.pack.emotelist:
            try:
                dpiLevels = None
                if isfile(self.pack.path + "/hidpi/" + emote.filename) and not emote.filename.endswith(".gif"):
                    with Image.open(self.pack.path + "/" + emote.filename) as orig:
                        origSize = orig.size;
                    self.perform_resize(emote, origSize, 2, outzip)
                    self.perform_resize(emote, origSize, 3, outzip)
                    dpiLevels = [2, 3]

                outzip.write(self.pack.path+"/"+emote.filename, "emotes/" + emote.filename)
                emotes[emote.filename] = {
                    "aliases": emote.shortcuts,
                    "width": emote.width,
                    "height": emote.height
                }
                if dpiLevels is not None:
                    emotes[emote.filename]["hidpi"] = dpiLevels
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.writestr("emotes/emoticons.json", json.dumps({
            "version": 2,
            "name": self.pack.name,
            "description": self.pack.desc,
            "author": self.pack.author,
            "emotes": emotes
        }))
        outzip.close()

    def perform_resize(self, emote, origSize, scale, outzip):
        """Resize and add the HD versions"""
        name, ext = emote.filename.split('.')
        with Image.open(self.pack.path + "/hidpi/" + emote.filename ) as highres, BytesIO() as f:
            highres.resize([origSize[0] * scale, origSize[1] * scale], resample=Image.LANCZOS).save(f, format=ext)
            outzip.writestr("emotes/%s@%dx.%s" % (name, scale, ext), f.getvalue())