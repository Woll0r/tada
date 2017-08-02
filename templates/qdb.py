"""QDB plugin for Tada"""

import json
import os
import zipfile

from yapsy.IPlugin import IPlugin


class QdbBackend(IPlugin):
    """QDB plugin for Tada"""
    pack = None
    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Qdb] Building zip...")
        self.makezip()

    def makezip(self):
        """Create the emote zip file"""
        emotes = {shortcut: emote.filename for emote in self.pack.emotelist for shortcut in emote.shortcuts}
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-qdb.zip", 'w')
        outzip.writestr(self.pack.name+"-qdbemotes/emotes.json", json.dumps(emotes))
        outzip.write(os.path.join(os.path.dirname(os.path.realpath(__file__)), "qdb-script.js"), self.pack.name+"-qdbemotes/emote-embed.js")
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+"-qdbemotes/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()
