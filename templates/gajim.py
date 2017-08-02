"""Gajim plugin for Tada"""

import zipfile
from pprint import pformat

from yapsy.IPlugin import IPlugin


class GajimBackend(IPlugin):
    """Gajim plugin for Tada"""
    pack = None
    emoticons = ""

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Gajim] Building emoticons.py...")
        self.buildemoticons()
        print("[Gajim] Building zip...")
        self.makezip()

    def buildemoticons(self):
        """Create the emote list to fill the config"""
        self.emoticons = "emoticons = "
        self.emoticons += pformat({emote.filename: emote.shortcuts for emote in self.pack.emotelist})

    def makezip(self):
        """Create the emote zip file"""
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-gajim.zip", 'w')
        outzip.writestr(self.pack.name+"-gajim/emoticons.py", self.emoticons)
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+"-gajim/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()
