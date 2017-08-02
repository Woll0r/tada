"""Conversations plugin for Tada"""

import json
import zipfile

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
                outzip.write(self.pack.path+"/"+emote.filename, "emotes/" + emote.filename)
                emotes[emote.filename] = {
                    "aliases": emote.shortcuts,
                    "width": emote.width,
                    "height": emote.height
                }
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
