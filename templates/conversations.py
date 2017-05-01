from yapsy.IPlugin import IPlugin
import zipfile
import json

class ConversationsBackend(IPlugin):
    pack = None

    def build(self, pack):
        self.pack = pack
        print "[Conversations] Building zip..."
        self.makeZip()

    def makeZip(self):
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
