"""Pidgin plugin for Tada"""

import zipfile

from yapsy.IPlugin import IPlugin


class PidginBackend(IPlugin):
    """Pidgin plugin for Tada"""
    pack = None

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Pidgin] Building zip...")
        self.makezip()

    def makezip(self):
        """Create the emote zip file"""
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-pidgin.zip", 'w')
        outzip.write(self.pack.path+"/theme", self.pack.name+"-pidgin/theme")
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+"-pidgin/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()
